# Automation source

| Script | Purpose | Default |
|---|---|---|
| lifecycle.py | Validate and reconcile approved HR state to IdP and target | Dry-run; --apply enables changes |
| governance.py | Validate temporary access decisions and write grant ledger | Dry-run; --apply enables changes |
| report.py | Export local target access and audit records | Writes private reports |

Run from iam-lab, using the manual's configured environment variables. Dry-run does not connect to or compare remote state. Read the prepared operational runbooks before applying changes. Do not run concurrent lifecycle copies.
