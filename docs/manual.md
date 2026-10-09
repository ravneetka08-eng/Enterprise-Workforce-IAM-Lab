# Workforce IAM Industry Skills Manual

A practical learning project for identity administration, SSO, provisioning, lifecycle automation and access governance

Version 1.0 • 2 October 2026 • Windows learning environment

## Start here

You will build and operate an identity environment for a fictional company called Northstar People. The company has Engineering, Finance and HR teams. Your job is to make employee access predictable, remove obsolete access, investigate failures and produce evidence a reviewer can understand.

This manual follows a learn, build, test and explain pattern. Read the definitions, carry out the numbered actions, perform both allowed and denied access tests, and record what actually happened. Do not mark a task complete because a configuration screen looks correct.

The core project runs locally with Keycloak, a working employee portal, a small SCIM provisioning target and Python automation. These are real protocol exchanges and enforced access controls using artificial employees. The HR input is a CSV rather than a commercial HRIS. The provisioning target implements a documented SCIM subset. The governance ledger is custom tooling rather than Okta Identity Governance. Those distinctions belong in your portfolio.

The optional Okta track gives you product-specific administration practice if you can obtain an Integrator Free Plan. Complete it after the core so signup eligibility does not prevent learning. This manual does not require paid trials, EC2, S3 hosting, Lambda, paid identity governance, a domain purchase or a public tunnel.

**What you receive:** the manual, portal source, lifecycle automation, governance commands, reporting commands, sample employee records, incident and change templates, test results and a JD mapping. Extract the supplied ZIP before starting. Commands assume its `iam-lab` directory is open in VS Code.

**How long:** allow approximately 30–45 hours over several weeks. This is a planning estimate, not a vendor promise. Spend additional time repeating failures and explaining your decisions.

**Start with Steps 0–4.** They establish your local identity system. Do not attempt every module in one sitting.

## The learning route

| Step | Outcome | Suggested effort |
|---|---|---|
| 0–2 | Scope, cost gate, tools and architecture | 3 hours |
| 3–5 | Identity directory, groups, OIDC and provisioning | 7 hours |
| 6–8 | Joiners, movers, leavers and MFA | 7 hours |
| 9–11 | SAML, approvals and access certification | 7 hours |
| 12–14 | Troubleshooting, AWS policies and operations | 5 hours |
| 15–17 | Optional Okta, evidence, cleanup and interview | 6 hours |

## Step 0 Define the business problem

**What we are doing:** translate the JD into access outcomes. In corporate work an IAM engineer starts with requirements, system owners and authoritative data, not a collection of users created without a purpose.

**Terms:** an identity is a representation of a person or workload. Authentication establishes who is signing in. Authorization decides what that identity may do. Provisioning creates or updates an account in a target system. Deprovisioning removes access; it does not always delete data. An identity provider, or IdP, authenticates users for other applications. An HRIS is a human resources information system that usually supplies employment status and organizational attributes.

1. Create `docs/scope.md` inside `iam-lab`.
2. Write the business problem: manual onboarding causes inconsistent access, department transfers leave old privileges, and leavers may retain application sessions.
3. Write the objective: reconcile approved HR records to IdP and portal access, prove removal, and document failures.
4. Name the scope: three artificial employees, one local portal, two identity realms for SAML, a local SCIM target and a manual approval ledger.
5. Name exclusions: production data, paid SaaS tenants, endpoint device compliance enforcement, commercial HRIS connectivity, enterprise high availability and regulated audit certification.
6. Assign simulated owners: HR owns employment status; department managers approve exceptional access; application owners define roles; IAM implements mappings; security reviews privileged access; an auditor reviews evidence. In this solo lab you act out these roles. This does not provide independently verified separation of duties.
7. Use `templates/change-record.md` to open CHG001 for the initial build. Document rollback as disabling the new client and restoring recorded settings, with database backup where necessary.

**Requirements to implement:** Engineering can access Engineering but not Finance; Finance can access Finance but not Engineering; movers lose the former department role; leavers cannot start new sessions and cannot use the portal through an existing session; temporary admin access expires; an inactive account is reviewed before deletion; failure is recorded instead of silently treated as success.

**Evidence:** scope document and first change record. **Checkpoint:** explain the difference between signing in successfully and being allowed to read Finance information.

## Step 1 Confirm the free tool boundary

**What we are doing:** choose a repeatable zero paid service design before enabling cloud features.

| Tool | Purpose | Free boundary |
|---|---|---|
| Keycloak | IdP, MFA, groups, sessions, OIDC and SAML | Local open-source software |
| Python and supplied code | Portal, provisioning, reconciliation and reports | Local software; no paid API |
| Docker Desktop Personal | Run Keycloak on Windows | Personal and education use under vendor terms [R1] |
| VS Code and Git | Edit files and record changes | Local tools; GitHub account optional |
| AWS IAM | Policy authoring and simulation | No compute resource is required |
| Okta Integrator Free Plan | Optional Okta administration and Workflows | Qualifying business email, 10 active users, 5 workflows [R2] |

1. Sign into AWS and open Billing and Cost Management. Record your account plan, expiry/credit information and current costs privately. Hide billing details from public screenshots.
2. Do not create or join AWS Organizations for this core project. AWS documents that creating an organization from a Free account plan upgrades the account to a paid plan and expires applicable Free Tier credits [R3]. This is different from saying IAM Identity Center itself has a service fee.
3. Do not assume a Free Tier eligible label makes every associated resource free. Public IPv4, storage, logs and usage above a limit can have separate pricing.
4. Protect your root account with MFA. Use your existing administrative identity for IAM setup. Never put root credentials into lab scripts.
5. Verify that optional Okta registration is possible at `https://developer.okta.com/signup/`. Use truthful registration details. If you lack an eligible business email, complete Keycloak; do not purchase a domain solely to continue.
6. Create `docs/cost-register.md`: local core = no paid cloud service required; AWS exercise = IAM policies and simulation only; optional Okta = free-plan feature check. Record an actual review date.

**Cost checkpoint:** no running AWS infrastructure is needed. Budget alerts, if you already use them, notify you; they are not an automatic universal spending cap.

## Step 2 Prepare Windows and understand the architecture

**Terms:** a container packages an application and its dependencies. A realm is an isolated identity namespace in Keycloak. Loopback means your own computer; `localhost` and `127.0.0.1` refer to it. A redirect URI is the exact address the IdP is allowed to send your browser back to after authentication. A bearer token gives access to whoever possesses it.

1. Close the existing VirtualBox lab VMs while using this project, especially if your computer has 16 GB RAM. This project does not need DC01 running.
2. Download Docker Desktop for Windows from the official Docker site [R1]. Select its WSL 2/Linux container setup. If requested, run `wsl --install` from Administrator PowerShell, restart Windows, and finish Docker setup. Only use Administrator PowerShell when Windows installation requires it.
3. Start Docker Desktop and wait for the engine to report that it is running. Run `docker version` in a normal PowerShell terminal. You should see client and server information. If only the client appears, the engine is not ready.
4. Install Python 3.12 or 3.13 from `https://www.python.org/downloads/windows/`. Enable the Python launcher during installation. Run `py --version`. A Microsoft Store prompt usually means Python or its path/launcher needs attention.
5. Install VS Code and Git if needed. Extract the ZIP into a folder such as `C:\Projects\Northstar-IAM`. Open the contained `iam-lab` folder with VS Code using File → Open Folder.
6. Open Terminal → New Terminal. Confirm your working folder ends in `iam-lab`. Run the following:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
New-Item -ItemType Directory -Force private
```

There is no need to activate the environment; the explicit Python path avoids PowerShell execution policy changes. `private` will hold local state, reports and logs that should not be committed automatically.

**Architecture:** HR snapshot → lifecycle script → Keycloak Admin API and SCIM HTTP API. The browser signs into Keycloak using OIDC and returns to the portal. The portal checks the provisioned account, department membership and temporary grants at each protected request. SSO alone does not create a portal account.

![The core identity architecture](architecture.png)

**Boundary:** Keycloak runs at `http://localhost:8080`; the portal runs at `http://localhost:5000`. The local HTTP exception is for an isolated development lab. Corporate deployments require HTTPS, trusted certificates, restricted management access, hardened application hosting, managed secrets and durable audit storage. Never expose these development services publicly.

**Evidence:** sanitized tool versions and architecture explanation. **Checkpoint:** explain why Okta hosted in the cloud cannot directly send SCIM requests to a service listening only on your laptop's localhost.

## Step 3 Build the identity directory and role model

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

## Step 4 Configure OIDC and start the employee portal

**What we are doing:** integrate a real relying application with the IdP. OIDC adds identity information to OAuth 2.0. OAuth itself is an authorization framework; it is not interchangeable with authentication.

**Terms:** a client is an application registered with the IdP. An authorization code is exchanged for tokens through the application's back channel. PKCE binds that exchange to the client that began the request. `state` helps protect the login redirect flow; `nonce` binds an ID token to the authentication request. An ID token is for the client to verify authentication; an access token is for an API to authorize access. Do not use an ID token as a generic API bearer credential.

1. In workforce → Clients → Create client, select OpenID Connect. Client ID: `employee-portal`. Name: Employee portal. Next.
2. Enable Client authentication and Standard flow. Disable Direct access grants and Implicit flow. Save.
3. In Access settings set Valid redirect URIs to exactly `http://localhost:5000/callback`. Set Home URL to `http://localhost:5000/`. Do not use a wildcard redirect. Save.
4. Open Advanced settings and set Proof Key for Code Exchange Code Challenge Method to S256 if that setting is exposed. The supplied client sends S256 PKCE. Keep the standard `profile` and `email` client scopes available.
5. Open Credentials. Copy the client secret privately. Do not commit it or place it in an evidence screenshot.
6. Before starting Terminal A, generate a SCIM token with `.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"`. Save it privately in a password manager. Then create Terminal A in VS Code, in `iam-lab`, and set the values below. Use fresh random secrets each time you rebuild the lab:

```powershell
$env:PORTAL_SECRET = .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
$env:SCIM_TOKEN = Read-Host 'Paste a random SCIM token generated and saved privately'
$env:OIDC_CLIENT_SECRET = Read-Host 'Paste the employee portal client secret'
$env:OIDC_CLIENT_ID = 'employee-portal'
$env:OIDC_DISCOVERY = 'http://localhost:8080/realms/workforce/.well-known/openid-configuration'
$env:AUTHLIB_INSECURE_TRANSPORT = '1'
.\.venv\Scripts\python.exe app\portal.py
```

7. Store the generated SCIM token in a password manager before launching the last command, or set it using a value generated and saved privately beforehand. Terminal B must use the same SCIM token. Do not rotate it between the two terminals accidentally. Environment variables are terminal-specific; they are not a vault.
8. Open `http://localhost:5000`. You should see Employee portal and Sign in with SSO. The employee accounts do not exist yet; finish Step 6 before the first successful employee login.
9. Keep Terminal A running. Its local development server is intentional for the lab, with debug mode off and loopback binding. Do not ignore this hosting limitation in your README.

**Under the hood:** Authlib uses discovery metadata and verifies the token as part of the code flow. The portal stores only selected identity claims in its signed session cookie, not raw tokens. It imposes a five-minute local session age. Its local logout clears the application session, not the Keycloak session. HTTP cookies are not Secure in this loopback development configuration; production requires HTTPS and Secure cookies.

![Authentication and provisioning are different flows](flows.png)

**Evidence:** client settings with secret hidden and the portal home screen. **Checkpoint:** why does a successful SSO callback still return 403 when a target account has not been provisioned?

## Step 5 Inspect the provisioning API before automating it

**What we are doing:** examine real HTTP provisioning requests and understand their effects. SCIM is the System for Cross-domain Identity Management. SSO answers who the user is; SCIM maintains accounts and memberships in the target.

The supplied target implements Users and Groups with creation, retrieval, replacement, deletion, simple equality filters, pagination and a limited replace PATCH. It uses SQLite for persistence and enforces a shared bearer token. It does not implement full SCIM discovery, bulk operations, full filter grammar, ETags or every PATCH path. Do not describe it as a certified connector. Keycloak core is not being used as a native SCIM server; Python bridges its Admin API and this SCIM target.

1. Open Terminal B. Use the same SCIM token from Terminal A:

```powershell
$env:SCIM_TOKEN = Read-Host 'Paste the saved local SCIM token'
$headers = @{Authorization = "Bearer $env:SCIM_TOKEN"}
Invoke-RestMethod -Uri 'http://localhost:5000/scim/v2/Users' -Headers $headers
```

2. Expect a SCIM ListResponse, initially with `totalResults` zero. Save a sanitized response in your evidence notes. Do not copy headers containing the bearer token.
3. Test an incorrect credential:

```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/scim/v2/Users' -Headers @{Authorization='Bearer deliberately-wrong'}
```

Expect HTTP 401; PowerShell presents this as an error. This is a passing negative test.

4. Leave target user creation to the lifecycle script. After Step 6, return and retrieve an account using a userName filter:

```powershell
$filter = [uri]::EscapeDataString('userName eq "alex.engineer@example.test"')
$u = Invoke-RestMethod -Uri "http://localhost:5000/scim/v2/Users?filter=$filter" -Headers $headers
$u.Resources
```

5. Inspect `id`, `externalId`, `userName`, `name` and `active`. The target's id is its internal identifier. externalId is E001, the HR correlation identifier. They are not interchangeable.
6. After saving your normal joiner evidence, use this explicit deactivation request for a later negative test:

```powershell
$id = $u.Resources[0].id
$body = @{schemas=@('urn:ietf:params:scim:api:messages:2.0:PatchOp'); Operations=@(@{op='replace'; path='active'; value=$false})} | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Patch -Uri "http://localhost:5000/scim/v2/Users/$id" -Headers $headers -ContentType 'application/scim+json' -Body $body
```

Do not deactivate E001 until you have tested normal access. Reapply the approved active HR snapshot in Step 6 to restore it. Record the deviation and reconciliation.

**Checkpoint:** explain HTTP 200, 201, 204, 400, 401, 403, 404, 409 and 429. A 401 is an invalid or missing credential; a 403 generally means the request is recognized but forbidden. A 409 duplicate requires reconciliation, not blindly retrying creation.

## Step 6 Build and run the joiner pipeline

**What we are doing:** provision employees from approved HR records. This is a complete local pipeline rather than an instruction to manually create users and call it automation.

1. In workforce → Clients → Create client, select OpenID Connect; client ID `hr-automation`.
2. Enable Client authentication and Service accounts roles. Disable Standard flow, Direct access grants and Implicit flow. Save.
3. Open Service account roles → Assign role. Filter by clients; select realm-management. Assign `manage-users`, `view-users`, `query-users` and `view-realm`. Do not assign realm-admin. Record that manage-users is still broad in this disposable realm; production should use finer scoped permissions where possible.
4. Copy the client secret from Credentials privately.
5. In Terminal B set:

```powershell
$env:KC_AUTOMATION_SECRET = Read-Host 'Paste the hr automation client secret'
$env:KC_BASE = 'http://localhost:8080'
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv
```

6. Expect a printed desired state for E001, E002 and E003, followed by DRY RUN. This validates CSV format and proposed state, not the current remote environment. No credentials are used until `--apply`.
7. Open `data/employees.csv`. Understand every field: employee_id stays stable; username is fixed in this lab; first_name and last_name are display data; department selects managed access; status is active or terminated. Only artificial `@example.test` identities are accepted.
8. Record the approved joiner change. Then execute:

```powershell
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv --apply
```

9. Expect `VALIDATED E001`, `VALIDATED E002`, `VALIDATED E003`. In Keycloak → Users verify three users, enabled status, employeeId and the expected groups. Inspect the SCIM target using Step 5.
10. In each Keycloak employee's Credentials tab choose Set password. Use a different strong local lab password and set Temporary on so the employee must change it at first login. The script deliberately does not create, email or log passwords.
11. Open a private browser window and sign into the portal as Alex. Change the temporary password if requested. Home should display employees and dept-engineering. Engineering should return 200; Finance should return 403. Repeat with Priya and Lee. HR should not receive either department resource.
12. Run the same apply command again. Confirm no additional users or groups appear and membership is unchanged. This is idempotency: applying the same intended state should not duplicate identities.

**Script behaviour:** it validates input before writes, correlates employee IDs, creates missing active identities, updates approved managed groups, provisions target accounts, reads both systems back and logs success only after state validation. It does not delete a person just because they are absent from the CSV. Absence is ambiguous; terminated is an explicit instruction. It manages four groups and leaves other groups alone.

**Failure boundary:** reconciliation is not an atomic transaction across systems. A later failure can leave earlier changes applied. The script stops with a failure record. Read the affected identity in both systems, repair the cause and rerun the same approved snapshot. It retries limited HTTP 429 and server errors with backoff; it stops on connection uncertainty. Never blindly replay an uncertain create—look for the existing identity first. It is single-runner tooling; do not execute concurrent copies.

**Evidence:** approved snapshot, sanitized successful run, Keycloak group membership, target account, allowed/denied tests and rerun count. **Checkpoint:** distinguish a real vendor HRIS connector from a CSV that emulates the authoritative HR source.

## Step 7 Operate a mover and remove obsolete access

**What we are doing:** transfer Alex from Engineering to Finance. Giving the new access without removing old access creates privilege accumulation.

1. Save a copy of the original CSV as `data/employees-before-move.csv`.
2. Open a mover request in your change record: E001 transfers to Finance; effective immediately in the lab; manager approves; Engineering access is no longer justified.
3. In employees.csv change only Alex's department from engineering to finance. Keep E001 and username unchanged.
4. Run dry-run. Check that E001 now requires dept-finance. Run with `--apply` after checking the proposed state.
5. In Keycloak and SCIM Groups verify E001 is in employees and dept-finance, absent from dept-engineering.
6. Keep Alex's previously open portal session. Refresh Engineering: expect 403. Open Finance: expect 200. If five minutes elapsed, sign in again and repeat.
7. Read the existing OIDC session explanation: the portal uses current target membership at each protected request. This avoids trusting a stale department claim in an older token for its resource decisions.
8. Document the effective change time, old role removal, new role addition, tests and rollback. Rollback means restoring the approved previous department and reconciling; it is not simply adding both groups.

**Evidence:** before/after role matrix and HTTP results. **Checkpoint:** why can a mover still have a valid identity session while no longer being authorized for their old resource?

## Step 8 Operate a leaver and practise MFA support

### Remove employee access

1. Keep Priya logged into the Finance resource in a private window.
2. Create an authorized leaver record for E002. State the lab target: block new sign-in and protected portal access after completed reconciliation. In production the required timing comes from risk, HR process and contracts.
3. Set Priya's status to terminated in employees.csv; do not delete the row. Run dry-run and apply.
4. Check Keycloak enabled is false and managed group memberships are gone. The script disables the IdP before downstream cleanup and requests Keycloak session logout.
5. Check target `active` is false and managed groups are gone.
6. Refresh Priya's existing portal Finance page. Expect 403 even if the local app cookie has not expired. Open a fresh private window and attempt IdP sign-in: it should fail.
7. Export evidence and retain the account record. Deactivation and deletion are separate decisions; employee documents or ownership may need retention and transfer.
8. Run `automation/report.py` in Step 11 and look for any still-live temporary grants. Active-check enforcement prevents a disabled user using them, but clean up the ledger too. Offboarding is not complete until exceptional grants, tokens and other applications are reviewed.

**Important:** ending an IdP session does not universally revoke every issued access token, every SaaS session or every application cookie. This portal rejects deactivated accounts through its own live check. A production leaver plan must include target-specific session and token behaviour, revocation capabilities, service ownership and credential rotation.

### Enrol and recover MFA

**Terms:** MFA combines factors from distinct categories, such as a password and a possession factor. TOTP is a time-based one-time password. TOTP improves on password-only login but is not phishing resistant. WebAuthn/passkeys or security keys may provide phishing resistant authentication.

1. In workforce → Authentication → Required actions enable Configure OTP. In Users → Alex → Details add Configure OTP to Required user actions; save. Do the same for each active employee. The supplied script preserves existing user settings rather than defining these required actions.
2. Open Authentication → Flows → browser and inspect the OTP step. Ensure the standard browser flow's conditional OTP path is enabled so configured OTP is requested. Do not replace the flow without a separate change plan.
3. Sign Alex out of Keycloak using its Account Console Sessions page or administrator session logout, then open a new private window. Sign in, scan the OTP setup code with a free authenticator app and supply the code. Never save the QR code or shared seed as evidence.
4. Sign out and sign in again. Expect an OTP challenge. Test one wrong code and one correct code; record outcomes. If no OTP is requested, investigate the bound browser flow and saved credentials.
5. Simulate a lost phone with a help desk ticket. Verify the employee using a pre-established independent process, such as a callback to an already recorded number and manager confirmation. Do not rely only on an email from the person requesting the reset. In the lab this verification is role-played and documented.
6. In Users → Alex → Credentials remove the OTP credential, add Configure OTP as a required action, and end current IdP sessions. Re-enrol using a new secret.
7. Verify the new OTP works and the former seed no longer generates valid codes for this account. Capture credential reset event metadata, never the credential values.
8. Record the support ticket, verification method, administrator action, session handling and successful recovery. Discuss how phishing resistant authenticators and recovery policy would change the design.

**Checkpoint:** why is an MFA reset itself a sensitive privileged operation?

## Step 9 Build SAML federation between two realms

**What we are doing:** configure a second application identity boundary using signed SAML assertions. The workforce realm is the IdP; a new partner realm is the SAML service provider through identity brokering. This is an actual local SAML exchange, not a diagram-only exercise. It is not a commercial SaaS integration.

**Terms:** an assertion is an IdP's signed statement about authentication and attributes. The Assertion Consumer Service, or ACS, receives the response. An entity ID identifies a SAML party. Metadata distributes endpoints and public signing certificates. A certificate rollover changes trusted keys and needs coordination. SAML signing certificates are different from HTTPS server certificates.

1. In the realm selector create `partner`. Keep registration off. Enable login/admin events as you did in workforce.
2. In partner → Identity providers → Add provider → SAML v2.0. Alias: `workforce-saml`. Display name: Workforce SAML.
3. In its import configuration use the workforce metadata URL:

```text
http://localhost:8080/realms/workforce/protocol/saml/descriptor
```

Select Import if shown, review the endpoints, enable Validate signature, and save. Keep signed assertions required. If a signing certificate is not populated, inspect the metadata's signing KeyDescriptor and import its X509Certificate into the validating certificate field. Public certificates can be shared; private keys cannot.

4. In the provider configuration copy the Redirect URI shown by Keycloak. It should be `http://localhost:8080/realms/partner/broker/workforce-saml/endpoint`. This is the ACS we need on the workforce client.
5. Set Service provider entity ID, if exposed, to `http://localhost:8080/realms/partner`. Record its exact value. Open the provider's SAML SP metadata endpoint:

```text
http://localhost:8080/realms/partner/broker/workforce-saml/endpoint/descriptor
```

6. Switch to workforce → Clients → Import client. Import the partner SP metadata XML by pasting its contents or saving and choosing it. This preserves compatible entity ID, ACS and signing configuration. If the import UI is absent, create a SAML client with Client ID equal to the SP entity ID and the ACS from action 4, then copy the metadata's certificates and settings deliberately.
7. In the SAML client verify Force POST binding is on, Sign assertions is on and Name ID format is username. Ensure signing settings match the imported metadata. If Client signature required is on, the partner provider must sign its requests and the workforce client must trust the partner's public key. Use metadata rather than turning signature validation off to hide an error.
8. Open `http://localhost:8080/realms/partner/account` in a new private window. Select Workforce SAML on the login screen. Sign in as Alex at workforce, including MFA. On first broker login complete the Review profile screen and supply artificial profile values if required. Do not auto-link an account just because an unverified email matches.
9. Verify a brokered Alex account appears in partner → Users → Federated identities with provider workforce-saml. Verify the workforce login event and the partner broker event. Partner access does not automatically inherit all workforce portal authorization; each application owns its entitlements.
10. Open browser Developer Tools → Network before logging in again. Observe the ACS POST and SAMLResponse field. Do not publish the raw assertion: it contains identity/session data. Capture only sanitized endpoint names and a note that signature validation was enabled.
11. Negative test: temporarily set the validating certificate to an unrelated public certificate in partner, using a recorded change. New SAML sign-in should fail. Restore the trusted metadata/certificate and retest. Keep recovery access through the master admin console.
12. Explain a planned rollover: import the new trusted key before changing the IdP signer, maintain overlap where supported, test in a non-production environment, monitor failures, and retire the old key after the agreed overlap period.

**Evidence:** both realm settings, metadata trust relationship, successful brokered login, failed wrong-certificate test and restoration. **Checkpoint:** do not call a base64-decoded assertion verified until the signature, issuer, audience, destination and time conditions have been validated.

## Step 10 Implement temporary access requests and expiry

**What we are doing:** add an approval-controlled entitlement with automatic runtime expiry. A ticket saying approved is insufficient unless something enforces the decision.

The supplied governance command reads requests, rejects self-approval, checks a reviewer allowlist, allows only portal-admin and limits new grants to at most one hour. It stores the expiry in the target database. The portal checks the grant and active account on every admin request. Reviewer identity is supplied in a local CSV by the operator; it is not independently authenticated. A corporate version needs an authenticated request interface, verified approver identity, resource owner rules, tamper-resistant history and service boundaries.

1. Restore Alex to active if you previously terminated Alex. Priya can remain terminated.
2. Open `data/requests.csv`. Keep request_id REQ001, username Alex, entitlement portal-admin and reviewer manager.engineering@example.test. Write a meaningful business justification.
3. Generate an expiry five minutes in the future:

```powershell
.\.venv\Scripts\python.exe -c "import time; print(int(time.time()+300))"
```

4. Replace REPLACE_WITH_FUTURE_EPOCH in requests.csv with that number. Unix epoch is seconds since 1 January 1970 UTC. Generate it immediately before the test.
5. Before applying the request, Alex's `/admin` page should return 403. Run:

```powershell
.\.venv\Scripts\python.exe automation\governance.py data\requests.csv
.\.venv\Scripts\python.exe automation\governance.py data\requests.csv --apply
```

6. Expect Alex's `/admin` page to return 200 after approval. After expiry it must return 403, without any manual group removal. If the five-minute local session expires, sign in again and verify the grant is still denied.
7. Test self-approval using a copy of requests.csv with reviewer equal to Alex. The command must reject it; no new grant should appear.
8. Test an unknown reviewer, missing justification and expiry more than an hour away. Each must fail. Use different request IDs for genuinely different requests; reusing REQ001 with changed values is rejected.
9. Revoke a valid unexpired request by setting decision to revoke and running apply. Record the original request, approval, enforcement result and revocation. Do not edit historical evidence to pretend the earlier access never existed.

**Evidence:** sanitized request ledger, pre-approval denial, approved access, expiry denial and negative tests. **Checkpoint:** distinguish operational expiry enforcement from a scheduler that merely emails someone when access should end.

## Step 11 Run access certification and licence review

**What we are doing:** review who has access, whether it remains justified, and whether remediation was completed. Certification is a business decision supported by data, not simply exporting users.

1. Run:

```powershell
.\.venv\Scripts\python.exe automation\report.py
```

2. Open `private/access-review.csv` in VS Code or a spreadsheet program. It includes target user, employee ID, active flag, group access, valid temporary grants, last observed portal use and blank reviewer decisions.
3. For each active user's department group, act as the resource owner: retain if business access is justified; revoke if obsolete; investigate if employment or owner information is missing. Fill reviewer, decision and reason.
4. Compare the review to the current HR snapshot, Keycloak membership and exceptional grant ledger. This report only covers this portal; it does not prove all SaaS systems were reviewed.
5. To remediate department access, change the approved HR record and reconcile through lifecycle.py. Do not just remove the target group if the next sync would restore it.
6. To remediate temporary access, use the revocation path in Step 10. To remediate an incorrect IdP-only exceptional role, record a separate owner-approved change and verify its removal.
7. Export a second report after remediation. Record each finding's before state, decision, owner, change reference and verified after state. Unresolved items must have an owner and due date.
8. Review inactivity flags: never_observed is not proof that an account is unused; it may be new or have missing telemetry. over_30_days means this target has no observed activity in that window. Confirm the HR status and business owner before reclaiming a licence or disabling an account.
9. Create `docs/licence-review.csv` with application, user, observed usage window, evidence source, licence assumption, owner, decision and verification. The portal has no paid licence; monetary savings are not measured. Do not invent a dollar saving.
10. Create `docs/oauth-inventory.csv` with client_id, owner, purpose, approved_scopes, redirect_uris, grant_types, service_account, review_date and decision. Populate it from workforce → Clients. Investigate broad redirect wildcards, unexpected direct grants, unused clients and unowned service accounts.
11. Create a disposable client `unapproved-demo` with no permissions, record it as an unapproved client finding, and remove it after review. This demonstrates inventory review, not enterprise discovery of every shadow IT application.

**Audit evidence:** private/audit.csv contains target changes and permitted resource access; private/lifecycle.jsonl contains reconciliation outcomes. Export matching Keycloak events from the admin UI where available, or capture filtered event details. Include UTC times, actor, target, action, result and source. Keep original evidence privately and publish only sanitized copies.

**Integrity:** local SQLite and CSV can be altered by the operator. Hashes detect later changes against a known recorded value but do not establish authenticity on their own. Corporate evidence needs restricted retention, independent logging and a defined chain of custody.

**Checkpoint:** access certification, licence utilization and SOC 2/ISO 27001 compliance are different things. This lab produces useful evidence examples; it does not establish organizational compliance or perform a certified audit.

## Step 12 Troubleshoot deliberately and write incident records

**What we are doing:** own the service when it fails. Corporate IAM work includes determining whether the fault is authentication, authorization, provisioning, source data or a session boundary.

Use templates/incident-record.md for each exercise. Record impact first, then evidence and hypotheses. Change one variable at a time and retest. Never paste secrets into an incident ticket.

| Failure exercise | How to reproduce safely | Expected diagnosis |
|---|---|---|
| Redirect mismatch | Change the portal client's callback to an incorrect local path | OIDC request rejected; exact callback must match |
| Unprovisioned account | Create a disposable employee in IdP only and try portal | Authentication can succeed; target authorization denies |
| Invalid SCIM bearer | Put wrong SCIM_TOKEN in Terminal B only | 401; IdP may already have partial changes |
| Bad HR department | Change department to marketing in a copy of CSV | Validation failure before writes |
| Duplicate employee ID | Duplicate E001 in a copy of CSV | Whole input rejected before writes |
| Target unavailable | Stop only the portal and run one approved snapshot | Failure logged; restore and reconcile |
| Wrong SAML trust | Use unrelated public validating certificate | Signature validation failure |
| Stale temporary grant | Wait until request expiry | Portal denies admin access |

1. Restore normal access first; confirm your baseline tests are green.
2. Reproduce one failure using a copy of input or a reversible configuration change. Leave the original approved data intact.
3. Check browser timestamp and HTTP status; Keycloak event error; target audit and pipeline status. Determine the first failing boundary.
4. State at least two plausible hypotheses and the evidence that eliminates one. Example: a redirect mismatch differs from a bad password because the IdP rejects the client request before an employee authenticates.
5. Apply the minimum corrective change. If provisioning failed after IdP writes, compare both systems and rerun the approved snapshot. Do not report success until read-back validation and user access tests pass.
6. Record rollback, retest, user impact, root cause and prevention. Prevention might be exact callback configuration in a change checklist or a dry-run input validation gate.
7. Classify priority from impact, not from the colour of an error banner: one lab employee missing a role differs from every employee unable to sign in.

**Challenge:** explain how to handle an API 429 without creating duplicate accounts, and how you would reconcile an ambiguous network timeout after a create. Look up the employee by stable identifier before replaying a write. A complete production implementation also needs a queue, dead-letter handling, alerts, concurrency control and more detailed correlation IDs.

## Step 13 Learn AWS least privilege without launching servers

**What we are doing:** author and test an identity policy for department-scoped read access. This is AWS IAM practice separate from workforce IdP administration. No bucket or EC2 instance is created, so this exercise does not incur infrastructure usage from those services.

**Terms:** ARN is an Amazon Resource Name. An identity policy is attached to a principal; a trust policy controls who may assume a role. Explicit deny overrides allow. If no applicable allow exists, the result is an implicit deny. The JSON Version 2012-10-17 selects the policy language version; it is not a certification that the policy is current or secure.

1. Sign into your existing AWS administrative identity with MFA. Open IAM → Policies → Create policy → JSON. Do not create a new root access key.
2. Paste this policy. The fictional bucket name represents a resource for simulation only:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListApprovedPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::northstar-iam-training-example",
      "Condition": {"StringLike": {"s3:prefix": ["engineering", "engineering/*"]}}
    },
    {
      "Sid": "ReadEngineeringObjects",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::northstar-iam-training-example/engineering/*"
    }
  ]
}
```

3. Inspect validation messages. Save as `NorthstarEngineeringReadLab` with a description explaining its simulation-only target. Do not attach it to your administrator.
4. Open IAM's current policy simulator feature from the IAM console. AWS moved the maintained simulator into IAM in July 2026 [R4]; old tutorials may show the standalone site.
5. Select a custom policy test if available and supply the policy. If the UI requires a principal, create a lab IAM user `northstar-policy-test` with no console password and no access keys, attach only this policy, and select it in the simulator. This user exists to evaluate policy; it is not your recommended production workforce identity pattern.
6. Run GetObject against `arn:aws:s3:::northstar-iam-training-example/engineering/handbook.txt`: expect allowed. Finance/handbook.txt: expect implicit deny. PutObject against Engineering: expect implicit deny.
7. Run ListBucket on the bucket ARN with s3:prefix set to engineering/: expect allowed. Repeat with finance/: expect implicit deny. The bucket ARN and object ARN are different; using the wrong ARN can invalidate the test.
8. Save the policy and simulation results to evidence. Label results as policy evaluation, not a successful live S3 request. The simulator does not create the bucket or prove all real-world access paths. Real access also depends on applicable resource policies, boundaries, organization controls and other context.
9. Delete the disposable principal after detaching the policy. Keep the policy until you finish the evidence, then delete it too.

**Optional existing-environment federation:** if you already have an appropriate IAM Identity Center organization instance and are willing to use it within your existing account setup, consult AWS's Okta SAML/SCIM integration guide [R5]. An account instance does not provide the same AWS account permission-set capabilities. This extension is not required for the free core and is not a reason to enable Organizations.

**Checkpoint:** explain why creating an IAM user with permanent access keys is not equivalent to federated workforce access using temporary role credentials.

## Step 14 Operate the environment like an IAM service

### Define the operational runbooks

1. Create docs/runbooks.md with five procedures: onboard employee, move department, offboard employee, verified MFA reset and failed provisioning recovery. Each must have trigger, approved source, owner, prechecks, exact command or UI path, validation, exception handling and evidence.
2. Create docs/service-objectives.md with illustrative local objectives: scheduled onboarding ready before start; authorized urgent leaver action immediately upon receipt; failed reconciliation escalated before access is marked complete. State that actual corporate SLAs require business agreement, time coverage and tooling capacity.
3. Create docs/exception-register.csv with exception ID, identity, resource, reason, approver, start, expiry, compensating control, review owner and status. An exception without expiry is an unresolved risk, not a permanent workaround.
4. Create docs/risk-register.csv. Record broad automation permissions, local HTTP, operator-editable evidence, missing independently verified approver identity, absent commercial HRIS connector and no device compliance enforcement. For each record likelihood, impact, treatment, owner, validation and residual risk. Explain your scales; do not invent precision.

### Back up and recover

1. Stop the portal using Ctrl+C in Terminal A before copying its SQLite database, so you do not copy during a write. Copy `private/portal.db` to a dated file under private. Reopen the portal afterward with the same saved settings.
2. Stop Keycloak with `docker stop northstar-kc`. Use a local helper container to archive the named volume to a private host directory:

```powershell
$backupPath = (Resolve-Path private).Path
docker run --rm --mount 'type=volume,source=northstar-kc-data,target=/data,readonly' --mount "type=bind,source=$backupPath,target=/backup" alpine:3.22 tar czf /backup/keycloak-volume.tgz -C /data .
docker start northstar-kc
```

3. Treat the archive as secret-bearing identity data. Do not commit it. Keep the pinned image version recorded alongside it. A realm configuration export alone does not prove a full recovery of users, credentials and sessions.
4. For a restore rehearsal, keep the primary lab stopped. Restore the archive into a different new volume, create a separate container with the same image on loopback port 8081, and verify the realms and user records. Example:

```powershell
docker volume create northstar-kc-restore
docker run --rm --mount 'type=volume,source=northstar-kc-restore,target=/data' --mount "type=bind,source=$backupPath,target=/backup,readonly" alpine:3.22 tar xzf /backup/keycloak-volume.tgz -C /data
docker run -d --name northstar-kc-restore -p 127.0.0.1:8081:8080 -v northstar-kc-restore:/opt/keycloak/data quay.io/keycloak/keycloak:26.8.0 start-dev
```

5. Inspect `http://localhost:8081` privately. Stored localhost:8080 callbacks will not automatically match a moved environment; this test initially verifies directory recovery, not complete federation recovery. A complete recovery drill must deliberately adjust callbacks/issuer dependencies and retest the affected applications. Delete only the rehearsal container/volume when done and restart the primary.
6. Record backup time, restoration time, validation and limitations. A created backup file is not evidence that recovery works.

### Assess device trust honestly

Write a design exercise: managed device state would come from a trusted endpoint management system; the IdP would enforce device assurance or equivalent policies; recovery and exception paths would be defined. This project does not implement Jamf, Island, Google Workspace or Entra device compliance. Browser headers are not a trustworthy replacement for managed device posture.

## Step 15 Add the optional Okta administration track

This track adds direct product experience where the free org exposes the required features. Keycloak remains your complete fallback. Do not claim Okta experience for modules you performed only in Keycloak. The free-plan feature list includes SSO, directory, adaptive MFA, lifecycle management, API access management and Workflows; full Okta Identity Governance is not listed [R2]. Do not activate a paid upgrade to follow this manual.

### Set up the directory and policies

1. Register an Integrator Free Plan at the official developer signup. Verify your tenant type and limits. Keep total active users, including administrators, within ten.
2. Preserve the original administrator and its enrolled recovery methods. Create up to three artificial employee accounts through Directory → People → Add person. Set activation/password options appropriate for a manual lab account; example.test addresses cannot receive real activation email.
3. Directory → Groups → Add group: create employees, dept-engineering, dept-finance and dept-hr. Assign the artificial users according to the role matrix.
4. Add profile attributes for employee ID and department using Directory → Profile Editor → Okta user profile. Choose string attributes and restrict who can modify authoritative fields. Record mappings and source ownership.
5. In Security → Authenticators inspect available password, Okta Verify and phishing resistant options. Configure an employee enrolment policy for the lab groups. Keep the only administrator out of experimental policies until recovery is verified.
6. In Security → Authentication Policies create an employee portal policy requiring available appropriate factors. In Global Session Policy configure and record a limited session lifetime. Test with a non-admin employee using a fresh browser session; existing session state can hide an intended challenge.
7. Simulate a verified MFA reset in Directory → People → employee → authenticator reset action. Re-enrol and capture sanitized System Log events. Exact labels vary by tenant engine/version; use the user profile's reset actions rather than looking for a factor in a different user's account.

### Connect the supplied OIDC portal to Okta

1. Applications → Applications → Create App Integration → OIDC → Web Application.
2. Name Northstar employee portal; select authorization code grant. Set sign-in redirect URI `http://localhost:5000/callback`. Assign only the approved lab employee groups. Do not select everyone for convenience.
3. Record the client ID and secret privately. Use the tenant's org authorization server discovery endpoint:

```text
https://YOUR-OKTA-DOMAIN/.well-known/openid-configuration
```

4. In app claims or authorization server claim configuration supported by your tenant, ensure the ID token provides `preferred_username` equal to the target userName. For an org authorization server this may require an application profile/claim mapping. The supplied portal intentionally refuses identity tokens missing this claim. If the tenant does not allow it, make a reviewed portal mapping change using a verified claim such as email only when its value is controlled, unique and identical to the synthetic username; do not silently fall back to arbitrary claims.
5. Stop Terminal A. Change OIDC_CLIENT_ID, OIDC_CLIENT_SECRET and OIDC_DISCOVERY to the Okta values; keep the existing SCIM token and portal secret. Restart the portal. Remove AUTHLIB_INSECURE_TRANSPORT if desired for the remote HTTPS IdP; local HTTP callbacks remain a development exception that the provider must support.
6. Provision matching synthetic usernames into the local target using the established lab pipeline or explicit SCIM requests. This target provisioning is still the local Python path, not native Okta provisioning. Sign into the portal via Okta and test allowed and denied access.
7. Unassign one disposable test user from the Okta app and test a fresh login. Separately deactivate the matching target account and test an existing app session. Record the different behaviours. Restore approved assignments afterward.
8. Before returning to the core labs, restore the workforce discovery URL and client credentials in Terminal A. Keep evidence labelled with the IdP used.

### Practise SAML with Okta as the IdP

1. Use the partner realm from Step 9 but add a separate SAML identity provider alias `okta-saml`. Copy its ACS and SP entity ID from the provider and its descriptor; do not overwrite workforce-saml.
2. In Okta create a SAML 2.0 application. Set Single sign-on URL to the partner provider ACS, Audience URI to its SP entity ID, Name ID format to EmailAddress and application username to the controlled synthetic username. Ensure response/assertion signatures are enabled as supported.
3. Assign only the lab employee group. Export IdP metadata from Okta's Sign On setup/instructions and import it into partner's okta-saml provider. Require signature validation and trust the metadata signing certificate.
4. In the partner account login choose the Okta provider. Complete sign-in and check partner's federated identity link and both systems' events. Existing auto-link policy must not let an unverified email take over an existing account.
5. Repeat the certificate mismatch and repair exercise, preserving administrator recovery access. Record this separately as an Okta SAML integration.

### Build an Okta Workflows exercise

1. Open Workflows from the admin console if available. Connect the Okta connector using the free org's supported authorization setup. Use only required permissions and record the integration owner.
2. Create a scheduled flow named Northstar joiner reconciliation. Add a Workflows table with employee_id, username, department, status and processed fields. Enter one synthetic joiner row.
3. Add table search for unprocessed rows and process each using a helper flow. Before creating a user, use the Okta connector to search or read the intended identity. If present, update the intended attributes rather than create another identity. Use employee_id as the correlation attribute.
4. For active rows, create/update the user and add the mapped department group. For movers, remove old managed department groups before adding the new group. For terminated rows, deactivate the test identity, remove assigned app access as required by connector behaviour and verify the intended target result before marking processed.
5. Add explicit error handling in the editor: leave processed false, record employee ID and error category in a failure table, and investigate before retry. Never record passwords or API tokens. Inspect actual connector card inputs/outputs because card names vary with connector version.
6. Keep the total including helper flows within the five-flow limit. Suggested allocation: one scheduler, one reconciliation helper, one error helper, one review export and one spare. Start with only the scheduler and reconciliation helper.
7. Test duplicate processing and a deliberately invalid group ID. Inspect execution history. Restore correct values and verify recovery. Mark processed only after a read-back of user status and expected group membership.
8. Export a sanitized flow diagram or capture card layout. Label this as a Workflows table acting as an HR source, not a production HRIS integration.

### Understand hosted SCIM limitations

Okta cannot connect to the local target at localhost. This manual deliberately avoids public tunnels and self-hosted public endpoints. You therefore have two separate pieces of evidence: local SCIM protocol implementation and, if eligible, Okta administration/integrations. Do not claim end-to-end Okta SCIM to this local target.

If an existing free supported application with accessible SCIM features is available to you later, onboard it using its documented endpoint, credentials and attribute mappings; test create, update, deactivate and separate app assignment from group push. Many SaaS products reserve SCIM for paid plans. Stop rather than upgrading when the exercise depends on such a plan. The supplied SCIM subset is not promised to be compatible with all native Okta Group Push operations.

**Governance boundary:** use Steps 10–11 for equivalent custom governance practice. If your free tenant lacks OIG, leave OIG as a learning gap. Do not call a Workflows access report an OIG certification campaign.

## Step 16 Build evidence and publish a defensible portfolio

**What we are doing:** turn completed tests into a portfolio that someone can review and that you can explain without memorizing every command.

1. Complete templates/test-results.csv with actual status, UTC time and evidence reference. Leave NOT RUN where appropriate. A denied access test can be PASS when denial was expected.
2. Keep raw logs, archives, tokens and screenshots containing credentials under private or evidence/raw. Put sanitized evidence under evidence. Synthetic names can be public; real account IDs, tenant identifiers and operational details should be assessed before publication.
3. Create docs/evidence-index.csv: evidence ID, requirement, system, timestamp UTC, expected result, observed result, sanitized file, reviewer and limitation.
4. Add a README explaining problem, architecture, how to reproduce, role matrix, implemented modules, actual tests, failure case, residual risks, cost boundary and cleanup. Do not state that you operated a real enterprise or passed a compliance audit.
5. Open a PowerShell terminal in iam-lab and use this Git sequence:

```powershell
git init
git status
git add README.md requirements.txt .gitignore app automation data templates docs evidence
git diff --cached
```

6. Review the staged content. Check that private, .env, databases, credentials and raw tokens are absent. `git diff --cached` reviews text; inspect staged images separately. Do not screenshot secret-bearing terminals.
7. Commit with `git commit -m "Add workforce IAM lifecycle lab and validated evidence"` only after the staged review. Change the description if tests are not completed.
8. Create an empty GitHub repository without a generated README if this is a new project. Copy its URL and run:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/workforce-iam-lab.git
git push -u origin main
```

9. If using an existing repository, inspect `git remote -v` and its history first. Do not re-add origin or force push over other work. Review unexpected remote commits before integrating them.
10. For subsequent updates run git status, add selected files, review the staged diff, commit and push. Open the repository as a visitor and check images, links and the README.
11. If a secret is committed, revoke/rotate it first, then follow the hosting provider's secret-removal process. Merely deleting the visible file does not remove it from history.

**Interview demonstration:** show Alex's allowed/denied access, a department move, a leaver using an existing session, temporary access expiry and one failed provisioning recovery. Explain authoritative source, correlation ID, least privilege, session limits, idempotency and evidence.

**Resume wording after completing the tests:** Built a local workforce IAM lab with Keycloak OIDC and SAML federation, Python HR lifecycle reconciliation, a SCIM provisioning subset, expiring access grants and access-review reporting; validated joiner, mover and leaver access outcomes. Add Okta product names only for the modules you actually complete.

You do not need to memorize the command syntax. You should understand the effect, dependencies, validation and recovery path and be able to find vendor documentation quickly.

## Step 17 Clean up and measure completion

1. Export and sanitize evidence before removal. Retain only private backups that you intentionally need.
2. Revoke outstanding temporary grants and remove optional Okta app assignments, clients and Workflows connections you no longer need. Disable/delete artificial users as appropriate. Keep access to your own administrator and recovery methods until tenant work is finished.
3. Stop the portal with Ctrl+C. Clear credential environment variables in each terminal or close the terminals. Closing a terminal does not delete secrets saved elsewhere.
4. Stop and remove only the named lab containers:

```powershell
docker stop northstar-kc
docker rm northstar-kc
```

5. If the restore rehearsal exists, stop/remove northstar-kc-restore separately. Once you are certain you no longer need identity state, remove `northstar-kc-data` and `northstar-kc-restore` volumes with `docker volume rm NAME`. This deletes the lab identities permanently. Do not run a broad prune against unrelated projects.
6. Delete or securely retain local private databases and backups according to your learning plan. Record what remains and why.
7. In AWS detach/delete the disposable policy principal and policy from Step 13. Check current costs and confirm no unexpected resources were introduced. Do not disable existing account security controls or delete unrelated IAM identities.
8. Complete a final report: implemented skills, passed and failed tests, known gaps, costs observed, cleanup performed and next learning goal.

**Completion criteria:** OIDC and SAML success plus failure tests; allowed and denied RBAC; joiner/mover/leaver read-back and browser tests; MFA enrolment and verified reset exercise; idempotency and partial failure recovery; request rejection and expiry; access review remediation; AWS simulation labelled honestly; evidence and cleanup. Optional Okta tests have their own completion status.

## Appendix A Key terms in plain language

| Term | Meaning |
|---|---|
| Identity governance | Deciding, approving and reviewing who should retain access |
| Federation | Trusting another identity provider to authenticate identities |
| SSO | Reusing an IdP authentication session across integrated applications |
| SCIM | A standard protocol for exchanging identity resources and updates |
| SAML | XML-based federation protocol using signed assertions |
| OIDC | Authentication layer using OAuth flows and identity tokens |
| OAuth scope | A requested or granted permission boundary for a client |
| JML | Joiner, mover and leaver lifecycle operations |
| Attribute mapping | Translating source identity fields to target fields |
| Group mapping | Translating business groups into target memberships or roles |
| Session | A maintained authenticated context in one system |
| Idempotency | Repeating intended state without duplicating identities or privileges |
| Reconciliation | Comparing intended and actual state and correcting differences |
| Access certification | Owner review of access with decisions and verified remediation |
| Least privilege | Granting necessary permissions and denying unrelated activity |
| Break glass | A controlled emergency access path with strong protection and review |
| Residual risk | Risk remaining after a treatment is implemented and validated |
| Audit evidence | Traceable records supporting a specific control assertion |

## Appendix B Skills against the job description

| JD area | What this project can prove | What remains outside the core |
|---|---|---|
| IdP administration | Keycloak directory, MFA, recovery and sessions | Production Okta operations |
| Application onboarding | Working local OIDC and SAML trust | Commercial SaaS end-to-end onboarding |
| SCIM | Provisioning HTTP subset and mapping tests | Certified connector and complete Group Push |
| HRIS lifecycle | CSV-to-IdP-and-target reconciliation | Commercial HRIS events and API integration |
| Okta Workflows | Optional free tenant exercise | Product experience if signup is unavailable |
| Governance | Expiring custom approvals and certification | OIG product configuration |
| Audit support | Sanitized identity and target evidence | An actual SOC 2 or ISO 27001 audit |
| SaaS governance | Inventory and inactivity review methods | Enterprise shadow IT detection and paid licence savings |
| Ancillary platforms | Integration boundaries and documented gaps | Jamf, Island, Google Workspace and Entra administration |

## Appendix C References and version notes

The lab configuration and workflow choices are educational design decisions. Vendor product limits and setup pages were checked on 2 October 2026. Interfaces change; follow the meaning of the setting and record the installed versions. Never bypass validation because a screenshot in an older tutorial differs.

[R1] Docker Windows installation and licence terms: https://docs.docker.com/desktop/setup/install/windows-install/ and https://docs.docker.com/subscription-billing/desktop-license/

[R2] Okta Integrator Free Plan configuration and limits: https://developer.okta.com/docs/reference/org-defaults/

[R3] AWS IAM Identity Center enablement and Free account plan warning: https://docs.aws.amazon.com/singlesignon/latest/userguide/enable-identity-center.html

[R4] AWS IAM policy simulator: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html and https://aws.amazon.com/about-aws/whats-new/2026/07/iam-policy-simulator-iam-console/

[R5] AWS Okta SAML and SCIM integration: https://docs.aws.amazon.com/singlesignon/latest/userguide/gs-okta.html

[R6] Keycloak container getting started: https://www.keycloak.org/getting-started/getting-started-docker

[R7] Keycloak administration and REST API: https://www.keycloak.org/docs/26.8.0/server_admin/ and https://www.keycloak.org/docs-api/26.8.0/rest-api/index.html

[R8] Authlib Flask OIDC client integration: https://docs.authlib.org/en/latest/oauth2/client/web/flask.html

[R9] SCIM protocol and schema: https://www.rfc-editor.org/rfc/rfc7644 and https://www.rfc-editor.org/rfc/rfc7643

[R10] Okta authentication/session policy, authenticator reset and event documentation: https://help.okta.com/oie/en-us/Content/Topics/identity-engine/policies/osop-evaluation.htm and https://help.okta.com/oie/en-us/content/topics/reports/report-types.htm

## Appendix D Validation of the supplied starter code

Local checks passed for SCIM credential rejection, account creation and duplicate rejection, supported filtering and PATCH, department allow/deny, deactivation with an existing app session, temporary grant expiry, governance rerun behaviour, self-approval rejection and HR dry-run validation. Live Keycloak, AWS and Okta integration tests were not executed in the authoring environment.

The starter is learning software. The manual's browser, Keycloak, AWS and optional Okta tests must be performed in your own accounts/environment and entered into test-results.csv. Do not treat the author's local source checks as evidence that your build passed. Before any corporate use, the software would need security review, stronger identity correlation, authenticated approval, strict schemas, complete SCIM behaviour, bounded concurrent processing, tested recovery, managed secrets and production hosting.
