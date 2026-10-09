"""Lab approval ledger; local operator supplies reviewer identity. Not identity-verified."""
import argparse,csv,sqlite3,time,os,json
p=argparse.ArgumentParser();p.add_argument('request_file');p.add_argument('--apply',action='store_true');a=p.parse_args()
rows=list(csv.DictReader(open(a.request_file,newline='',encoding='utf-8-sig')))
reviewers={'manager.engineering@example.test','manager.finance@example.test'}
db=os.environ.get('LAB_DB','private/portal.db')
with sqlite3.connect(db) as c:
    for r in rows:
        if r['decision'] not in ('approve','revoke'): raise ValueError('Invalid decision')
        if r['reviewer'] not in reviewers or r['reviewer']==r['username']: raise ValueError('Invalid reviewer or self approval')
        if r['entitlement']!='portal-admin': raise ValueError('Unapproved entitlement')
        if not r['reason'].strip():raise ValueError('Justification required')
        expires=float(r['expires_epoch'])
        if r['decision']=='approve' and not time.time()<expires<=time.time()+3600: raise ValueError('Expiry must be in next hour')
        u=[json.loads(v[0]) for v in c.execute("SELECT body FROM resources WHERE kind='Users'")]
        if not any(x.get('userName')==r['username'] and (x.get('active') or r['decision']=='revoke') for x in u): raise ValueError('User inactive or missing')
        print(r['decision'],r['request_id'],r['username'],'expires',expires)
        if a.apply:
            if r['decision']=='revoke':
                c.execute('DELETE FROM grants WHERE request_id=? AND username=?',(r['request_id'],r['username']))
            else:
                existing=c.execute('SELECT username,entitlement,expires FROM grants WHERE request_id=?',(r['request_id'],)).fetchone()
                desired=(r['username'],r['entitlement'],expires)
                if existing and existing!=desired: raise ValueError('Request ID reused with changed values')
                c.execute('INSERT OR IGNORE INTO grants VALUES(?,?,?,?)',(*desired,r['request_id']))
            c.execute("INSERT INTO audit VALUES(datetime('now'),?,?)",('GOVERNANCE '+r['decision']+' reviewer='+r['reviewer'],r['request_id']))
print('APPLIED' if a.apply else 'DRY RUN; no writes')
