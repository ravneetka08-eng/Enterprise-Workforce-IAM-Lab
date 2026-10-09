"""HR snapshot reconciliation. Dry-run is default. See manual before --apply."""
import os,csv,json,sys,time,argparse
from pathlib import Path
import requests
p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--apply',action='store_true');a=p.parse_args()
rows=list(csv.DictReader(open(a.csv_file,encoding='utf-8-sig',newline='')))
required={'employee_id','username','first_name','last_name','department','status'}
if not rows or not required<=set(rows[0]): sys.exit('Missing rows or required columns')
for field in ('employee_id','username'):
    if len({r[field] for r in rows})!=len(rows): sys.exit('Duplicate '+field)
for r in rows:
    if any(not r[f].strip() for f in required): sys.exit('Blank required value')
    if r['status'] not in ('active','terminated'): sys.exit('Unsupported status')
    if r['department'] not in ('engineering','finance','hr'): sys.exit('Unsupported department')
    if not r['username'].endswith('@example.test'): sys.exit('Only example.test identities permitted')
print(json.dumps([{'employee_id':r['employee_id'],'username':r['username'],'enabled':r['status']=='active',
                   'managed_group':'dept-'+r['department'] if r['status']=='active' else None} for r in rows],indent=2))
if not a.apply:
    print('DRY RUN: validated desired state only. No connections or writes.'); sys.exit(0)
base=os.environ.get('KC_BASE','http://localhost:8080');realm='workforce'
if base!='http://localhost:8080': sys.exit('This lab script permits only localhost Keycloak')
s=requests.Session();token=None; expiry=0

def kc_token():
    global token,expiry
    if time.time()>expiry:
        r=requests.post(base+'/realms/'+realm+'/protocol/openid-connect/token',data={
            'grant_type':'client_credentials','client_id':'hr-automation','client_secret':os.environ['KC_AUTOMATION_SECRET']},timeout=15)
        r.raise_for_status();b=r.json();token=b['access_token'];expiry=time.time()+b.get('expires_in',60)-10
    return token

def call(method,url,**kw):
    for attempt in range(4):
        r=s.request(method,url,timeout=15,**kw)
        if r.status_code==429 or r.status_code>=500:
            if attempt==3: r.raise_for_status()
            time.sleep(min(2**attempt,4)); continue
        # Do not automatically retry non-idempotent create after connection uncertainty.
        r.raise_for_status();return r

def kc(method,path,**kw):
    return call(method,base+'/admin/realms/'+realm+path,headers={'Authorization':'Bearer '+kc_token()},**kw)

def sc(method,path,**kw):
    return call(method,'http://localhost:5000/scim/v2'+path,
                headers={'Authorization':'Bearer '+os.environ['SCIM_TOKEN'],'Content-Type':'application/scim+json'},**kw)
Path('private').mkdir(exist_ok=True)
groups=kc('GET','/groups',params={'max':100}).json();gm={g['name']:g['id'] for g in groups}
managed={'employees','dept-engineering','dept-finance','dept-hr'}
if not managed<=set(gm): sys.exit('Create all managed Keycloak groups first')

for row in rows:
    username=row['username'];active=row['status']=='active';eid=row['employee_id']
    try:
        users=kc('GET','/users',params={'username':username,'exact':'true'}).json()
        if len(users)>1: raise RuntimeError('Ambiguous identity')
        if users:
            user=users[0]
            if user.get('attributes',{}).get('employeeId')!=[eid]: raise RuntimeError('Employee ID mismatch; manual review required')
            uid=user['id']
        else:
            if not active: raise RuntimeError('Terminated identity missing; investigate rather than create')
            response=kc('POST','/users',json={'username':username,'firstName':row['first_name'],
                'lastName':row['last_name'],'email':username,'emailVerified':False,'enabled':True,'attributes':{'employeeId':[eid]}})
            uid=response.headers['Location'].rstrip('/').split('/')[-1]
        # Disable sign-in before downstream cleanup on a leaver.
        kc('PUT','/users/'+uid,json={'firstName':row['first_name'],'lastName':row['last_name'],
                                    'enabled':active,'attributes':{'employeeId':[eid]}})
        if not active: kc('POST','/users/'+uid+'/logout')
        desired={'employees','dept-'+row['department']} if active else set()
        current={g['name']:g['id'] for g in kc('GET','/users/'+uid+'/groups').json()}
        for name in (set(current)&managed)-desired: kc('DELETE','/users/'+uid+'/groups/'+current[name])
        for name in desired-set(current): kc('PUT','/users/'+uid+'/groups/'+gm[name])
        found=sc('GET','/Users',params={'filter':'userName eq "'+username+'"'}).json()['Resources']
        payload={'schemas':['urn:ietf:params:scim:schemas:core:2.0:User'],'externalId':eid,'userName':username,
                 'name':{'givenName':row['first_name'],'familyName':row['last_name']},'active':active}
        if len(found)>1: raise RuntimeError('Duplicate target users')
        if found:
            if found[0].get('externalId')!=eid: raise RuntimeError('Target employee ID mismatch')
            sid=found[0]['id']; sc('PUT','/Users/'+sid,json=payload)
        else:
            if not active: raise RuntimeError('Missing leaver target account')
            sid=sc('POST','/Users',json=payload).json()['id']
        for name in sorted(managed):
            gs=sc('GET','/Groups',params={'filter':'displayName eq "'+name+'"'}).json()['Resources']
            g=gs[0] if gs else sc('POST','/Groups',json={'displayName':name,'members':[]}).json()
            members=[m for m in g.get('members',[]) if m.get('value')!=sid]
            if name in desired: members.append({'value':sid,'display':username})
            sc('PUT','/Groups/'+g['id'],json={'displayName':name,'members':members})
        # Verify downstream state; do not mark complete just because PUT returned 200.
        verified=sc('GET','/Users/'+sid).json()
        if verified.get('active')!=active: raise RuntimeError('Target validation failed')
        actual=set()
        for g in sc('GET','/Groups').json()['Resources']:
            if any(m.get('value')==sid for m in g.get('members',[])): actual.add(g['displayName'])
        if actual & managed != desired: raise RuntimeError('Target membership validation failed')
        ku=kc('GET','/users/'+uid).json()
        kg={g['name'] for g in kc('GET','/users/'+uid+'/groups').json()}
        if ku.get('enabled')!=active or kg & managed != desired: raise RuntimeError('IdP validation failed')
        event={'time':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'employee_id':eid,'status':'validated',
               'enabled':active,'groups':sorted(desired)}
        with open('private/lifecycle.jsonl','a',encoding='utf-8') as f:f.write(json.dumps(event)+'\n')
        print('VALIDATED',eid)
    except Exception as e:
        # Keep credential-bearing responses out of the log.
        event={'time':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'employee_id':eid,
               'status':'failed','error_type':type(e).__name__}
        with open('private/lifecycle.jsonl','a',encoding='utf-8') as f:f.write(json.dumps(event)+'\n')
        print('FAILED',eid,type(e).__name__,'Stop and reconcile partial state.');sys.exit(1)
