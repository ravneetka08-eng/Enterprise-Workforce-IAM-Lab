# Access certification procedure

## Prepare the review

Run report.py to produce private/access-review.csv and private/audit.csv. Record export time, system scope and telemetry limitations. Compare each identity to the approved HR snapshot, current IdP membership and temporary grant ledger.

## Make a business decision

The role-played application owner selects retain, revoke or investigate with a reason. Never-observed usage is not sufficient evidence to disable an account. Review temporary privileged grants separately from standard department access.

## Remediate

Correct department access at the authoritative HR snapshot and reconcile; otherwise later automation may re-add a removed target group. Revoke temporary access through governance.py. Other exceptional access needs a separate approved change.

## Close

Export a second report, verify the changed access and connect before/after evidence to the change ID. Leave unresolved findings open with owner and due date. Do not describe a CSV export as completed certification until decisions and remediation are recorded.

**Execution date, decisions and outcomes: pending.**
