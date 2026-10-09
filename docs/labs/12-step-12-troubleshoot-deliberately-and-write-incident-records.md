# Step 12 Troubleshoot deliberately and write incident records

**Practical status: NOT STARTED.**


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
