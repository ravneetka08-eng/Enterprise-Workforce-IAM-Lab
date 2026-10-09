# Step 16 Build evidence and publish a defensible portfolio

**Practical status: NOT STARTED.**


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
