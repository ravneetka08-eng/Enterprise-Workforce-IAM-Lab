# Step 11 Run access certification and licence review

**Practical status: NOT STARTED.**


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
