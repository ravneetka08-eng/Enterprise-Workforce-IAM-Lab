"""Loopback-only IAM learning target. SCIM subset; never deploy publicly."""
import os, json, sqlite3, uuid, re, hmac, time
from functools import wraps
from flask import Flask, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from markupsafe import escape

app = Flask(__name__)
app.secret_key = os.environ['PORTAL_SECRET']
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
DB = os.environ.get('LAB_DB', 'private/portal.db')
os.makedirs(os.path.dirname(os.path.abspath(DB)), exist_ok=True)
SCIM_TOKEN = os.environ['SCIM_TOKEN']
BASE = 'http://localhost:5000/scim/v2'
USER_SCHEMA = 'urn:ietf:params:scim:schemas:core:2.0:User'
GROUP_SCHEMA = 'urn:ietf:params:scim:schemas:core:2.0:Group'
LIST_SCHEMA = 'urn:ietf:params:scim:api:messages:2.0:ListResponse'
PATCH_SCHEMA = 'urn:ietf:params:scim:api:messages:2.0:PatchOp'
ERROR_SCHEMA = 'urn:ietf:params:scim:api:messages:2.0:Error'
with sqlite3.connect(DB) as c:
    c.executescript('''CREATE TABLE IF NOT EXISTS resources(kind TEXT,id TEXT PRIMARY KEY,body TEXT);
    CREATE TABLE IF NOT EXISTS audit(ts TEXT,action TEXT,resource TEXT);
    CREATE TABLE IF NOT EXISTS grants(username TEXT,entitlement TEXT,expires REAL,request_id TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS activity(username TEXT PRIMARY KEY,last_seen REAL);''')

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def audit(c, action, rid):
    c.execute('INSERT INTO audit VALUES(datetime(\'now\'),?,?)',(action,rid))

def err(status, detail):
    return jsonify(schemas=[ERROR_SCHEMA],status=str(status),detail=detail),status

def protected(f):
    @wraps(f)
    def wrapped(*a,**k):
        expected = 'Bearer '+SCIM_TOKEN
        if not hmac.compare_digest(request.headers.get('Authorization',''),expected):
            return err(401,'Invalid provisioning credential')
        return f(*a,**k)
    return wrapped

@app.after_request
def headers(response):
    if request.path.startswith('/scim/'):
        response.headers['Content-Type']='application/scim+json'
    response.headers['Cache-Control']='no-store'
    return response

@app.route('/scim/v2/<kind>', methods=['GET','POST'])
@protected
def collection(kind):
    if kind not in ('Users','Groups'): return err(404,'Unknown resource type')
    with db() as c:
        rows=[json.loads(r['body']) for r in c.execute('SELECT body FROM resources WHERE kind=?',(kind,))]
        if request.method=='GET':
            filt=request.args.get('filter')
            if filt:
                match=re.fullmatch(r'(userName|displayName|externalId) eq "([^"\\]*)"',filt)
                if not match: return err(400,'Only simple equality filters supported')
                field,value=match.groups(); rows=[r for r in rows if r.get(field)==value]
            try:
                start=max(1,int(request.args.get('startIndex',1)))
                count=max(0,min(100,int(request.args.get('count',100))))
            except ValueError: return err(400,'Invalid pagination')
            selected=rows[start-1:start-1+count]
            return jsonify(schemas=[LIST_SCHEMA],totalResults=len(rows),startIndex=start,
                           itemsPerPage=len(selected),Resources=selected)
        body=request.get_json(force=True)
        key='userName' if kind=='Users' else 'displayName'
        if not isinstance(body,dict) or not body.get(key): return err(400,'Missing '+key)
        if any(r.get(key)==body[key] for r in rows): return err(409,'Resource already exists')
        if kind=='Users' and not isinstance(body.get('active',True),bool): return err(400,'active must be boolean')
        rid=str(uuid.uuid4()); body['id']=rid
        body['schemas']=[USER_SCHEMA if kind=='Users' else GROUP_SCHEMA]
        body['meta']={'resourceType':kind[:-1],'location':BASE+'/'+kind+'/'+rid}
        if kind=='Users': body.setdefault('active',True)
        c.execute('INSERT INTO resources VALUES(?,?,?)',(kind,rid,json.dumps(body)))
        audit(c,'CREATE '+kind,rid)
        response=jsonify(body); response.status_code=201; response.headers['Location']=body['meta']['location']
        return response

@app.route('/scim/v2/<kind>/<rid>',methods=['GET','PUT','PATCH','DELETE'])
@protected
def item(kind,rid):
    if kind not in ('Users','Groups'): return err(404,'Unknown resource type')
    with db() as c:
        row=c.execute('SELECT body FROM resources WHERE kind=? AND id=?',(kind,rid)).fetchone()
        if not row: return err(404,'Resource not found')
        body=json.loads(row['body'])
        if request.method=='GET': return jsonify(body)
        if request.method=='DELETE':
            c.execute('DELETE FROM resources WHERE id=?',(rid,)); audit(c,'DELETE '+kind,rid)
            return '',204
        incoming=request.get_json(force=True)
        if request.method=='PUT':
            key='userName' if kind=='Users' else 'displayName'
            if not incoming.get(key): return err(400,'Missing '+key)
            incoming.update(id=rid,schemas=body['schemas'],meta=body['meta']); body=incoming
        else:
            if PATCH_SCHEMA not in incoming.get('schemas',[]): return err(400,'Missing PatchOp schema')
            for operation in incoming.get('Operations',[]):
                if operation.get('op','').lower()!='replace': return err(400,'Only replace is implemented')
                path=operation.get('path'); value=operation.get('value')
                if path in ('active','displayName','name','members','userName'):
                    body[path]=value
                elif not path and isinstance(value,dict) and set(value)<= {'active','displayName','name','members','userName'}:
                    body.update(value)
                else: return err(400,'Unsupported patch path')
        if kind=='Users' and not isinstance(body.get('active',True),bool): return err(400,'active must be boolean')
        key='userName' if kind=='Users' else 'displayName'
        others=c.execute('SELECT body FROM resources WHERE kind=? AND id<>?',(kind,rid)).fetchall()
        if any(json.loads(r['body']).get(key)==body.get(key) for r in others): return err(409,'Duplicate name')
        c.execute('UPDATE resources SET body=? WHERE id=?',(json.dumps(body),rid)); audit(c,request.method+' '+kind,rid)
        return jsonify(body)

oauth=OAuth(app)
oauth.register(name='idp',client_id=os.environ.get('OIDC_CLIENT_ID','employee-portal'),
    client_secret=os.environ['OIDC_CLIENT_SECRET'],
    server_metadata_url=os.environ.get('OIDC_DISCOVERY','http://localhost:8080/realms/workforce/.well-known/openid-configuration'),
    client_kwargs={'scope':'openid profile email','code_challenge_method':'S256'})

@app.route('/login')
def login():
    return oauth.idp.authorize_redirect('http://localhost:5000/callback')

@app.route('/callback')
def callback():
    token=oauth.idp.authorize_access_token() # Authlib verifies ID token, state and nonce.
    info=token.get('userinfo')
    if not info or not info.get('sub') or not info.get('preferred_username'): return 'Required identity claims missing',403
    session.clear(); session['username']=info['preferred_username']; session['sub']=info['sub']; session['login_at']=time.time()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear(); return 'Local session removed. The identity provider session is separate. <a href="/">Home</a>'

def access_state():
    username=session.get('username')
    if not username: return None,None,[]
    if time.time()-session.get('login_at',0)>300:
        session.clear(); return None,None,[]
    with db() as c:
        users=[json.loads(r['body']) for r in c.execute("SELECT body FROM resources WHERE kind='Users'")]
        user=next((u for u in users if u.get('userName')==username),None)
        groups=[json.loads(r['body']) for r in c.execute("SELECT body FROM resources WHERE kind='Groups'")]
        memberships=[g['displayName'] for g in groups if user and any(m.get('value')==user['id'] for m in g.get('members',[]))]
    return username,user,memberships

@app.route('/')
def home():
    username,user,groups=access_state()
    if not username: return '<h1>Employee portal</h1><a href="/login">Sign in with SSO</a>'
    if not user or not user.get('active'): return 'Identity authenticated but local account inactive or unprovisioned',403
    with db() as c:
        c.execute('INSERT OR REPLACE INTO activity VALUES(?,?)',(username,time.time()))
    return f'<h1>Employee portal</h1><p>Signed in as {escape(username)}</p><p>Groups {escape(", ".join(groups))}</p><a href="/finance">Finance</a> | <a href="/engineering">Engineering</a> | <a href="/admin">Temporary admin access</a> | <a href="/logout">Local logout</a>'

@app.route('/<area>')
def area(area):
    if area not in ('finance','engineering','admin'): return 'Not found',404
    username,user,groups=access_state()
    if not username: return redirect('/login')
    if not user or not user.get('active'): return 'Account inactive or unprovisioned',403
    required={'finance':'dept-finance','engineering':'dept-engineering','admin':'portal-admin'}[area]
    allowed=required in groups
    if area=='admin':
        with db() as c:
            allowed=c.execute('SELECT 1 FROM grants WHERE username=? AND entitlement=? AND expires>?',
                              (username,'portal-admin',time.time())).fetchone() is not None
    if not allowed: return 'Access denied for '+area,403
    with db() as c:
        audit(c,'ACCESS '+area,user['id']); c.execute('INSERT OR REPLACE INTO activity VALUES(?,?)',(username,time.time()))
    return f'<h1>{escape(area.title())} resource</h1><p>Access permitted to synthetic demonstration data.</p><a href="/">Home</a>'

if __name__=='__main__': app.run(host='127.0.0.1',port=5000,debug=False)
