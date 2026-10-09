# Step 1 Confirm the free tool boundary

**Practical status: NOT STARTED.**


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
