# Step 17 Clean up and measure completion

**Practical status: NOT STARTED.**


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
