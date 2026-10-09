"""Local access certification and inactivity report; target scope only."""
import sqlite3,os,csv,json,time
from pathlib import Path
Path('private').mkdir(exist_ok=True)
with sqlite3.connect(os.environ.get('LAB_DB','private/portal.db')) as c:
    users=[json.loads(r[0]) for r in c.execute("SELECT body FROM resources WHERE kind='Users'")]
    groups=[json.loads(r[0]) for r in c.execute("SELECT body FROM resources WHERE kind='Groups'")]
    seen=dict(c.execute('SELECT username,last_seen FROM activity'))
    grants=list(c.execute('SELECT username,entitlement,expires,request_id FROM grants'))
    with open('private/access-review.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['username','employee_id','active','groups','temporary_grants','last_seen_epoch','inactivity_flag','reviewer','decision','reason'])
        for u in users:
            membership=[g['displayName'] for g in groups if any(m.get('value')==u['id'] for m in g.get('members',[]))]
            temp=[g[1] for g in grants if g[0]==u['userName'] and g[2]>time.time()]
            last=seen.get(u['userName']);flag='never_observed' if not last else ('over_30_days' if time.time()-last>30*86400 else 'recent')
            w.writerow([u['userName'],u.get('externalId'),u.get('active'),';'.join(membership),';'.join(temp),last,flag,'','',''])
    with open('private/audit.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['timestamp_utc','action','resource']);w.writerows(c.execute('SELECT * FROM audit ORDER BY ts'))
print('Wrote private/access-review.csv and private/audit.csv. Review and sanitize before publication.')
