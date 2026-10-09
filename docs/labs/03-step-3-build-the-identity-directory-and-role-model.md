# Step 3 Build the identity directory and role model

**Practical status: NOT STARTED.**


**What we are doing:** create the authoritative identity environment and group-based department mapping. We will create the first employees through the automation in Step 6, rather than duplicating identities manually.

**Terms:** RBAC is role-based access control. Groups represent business roles. Least privilege means granting the access needed for a task and verifying that unrelated access is denied. A service account represents automation rather than an employee.

1. In PowerShell set a strong temporary bootstrap administrator password. Keep it private:

```powershell
$env:KC_BOOTSTRAP_ADMIN_USERNAME = 'lab-admin'
$env:KC_BOOTSTRAP_ADMIN_PASSWORD = Read-Host 'Choose a local lab admin password'
docker run -d --name northstar-kc -p 127.0.0.1:8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME -e KC_BOOTSTRAP_ADMIN_PASSWORD -v northstar-kc-data:/opt/keycloak/data quay.io/keycloak/keycloak:26.8.0 start-dev
Remove-Item Env:KC_BOOTSTRAP_ADMIN_PASSWORD
```

`Read-Host` here is visible input: enter it when you are not screen sharing, and do not screenshot it. The image version is pinned for reproducibility; record any version change before troubleshooting. The local volume persists configuration across container stops. `start-dev` is not a production deployment.

2. Open `http://localhost:8080` and select Administration Console. Sign in as `lab-admin`. If unavailable, run `docker logs northstar-kc` and wait for startup. Do not create a second container as a workaround.
3. Use the realm selector → Create realm. Enter `workforce`, enable it, and create it. Confirm the selected realm says workforce before each change. Do not put employees in master.
4. Open Realm settings → Login. Keep user registration off and login with email off for now; usernames in this lab are email-shaped but we do not operate a mail server. Keep Forgot password off until an SMTP service is deliberately configured.
5. Open Groups → Create group. Create four top-level groups: `employees`, `dept-engineering`, `dept-finance`, `dept-hr`.
6. Open Realm settings → User profile. Add an attribute named `employeeId`, with display name Employee ID and multivalued off. Give administrators view/edit permissions. Do not give employees edit access. This lets the Admin API store a stable HR identifier. Save.
7. Open Realm settings → Events. Turn on Save events, include login and login-error events in saved types, and enable Save admin events. Keep Include representation off so secrets or excessive personal information are not stored in administrative event bodies. Choose a lab retention period, for example seven days, and record it.
8. Open Realm settings → Sessions. Set SSO session idle to 10 minutes and SSO session max to 30 minutes. These are illustrative lab values, not a universal corporate standard. Record the operational impact of shorter sessions.
9. Open Realm settings → Security defenses → Brute force detection. Enable protection; record the actual selected limits. Test later using an employee rather than the only admin. Keep an administrator recovery path available.

**Role matrix:** employees receive portal access only after provisioning; Engineering receives `dept-engineering`; Finance receives `dept-finance`; HR receives `dept-hr`. No employee receives realm administration rights. Temporary `portal-admin` is governed separately by an expiring grant, not the department mapping.

**Evidence:** group list, employeeId definition, event settings and session settings. **Checkpoint:** why should a user not be able to edit their own department or employment status?
