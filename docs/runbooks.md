# Operational runbooks

**Status: prepared procedures. All executions and outcomes pending.**

Run commands from the iam-lab root. See the manual for credential setup and UI details.

## Onboard an employee

**Trigger:** Approved active HR row and simulated manager request. **Owner:** IAM operator, with HR/application-owner approval as applicable. **Manual:** Step 6.

**Prechecks:** Validate CSV, employee ID uniqueness, department mapping and service credentials. Confirm approved groups exist.

**Actions:** Run lifecycle dry-run; inspect desired state; run --apply; set the new user's temporary password privately in Keycloak.

**Validation:** Read enabled/active state and both group sets. Test allowed and denied portal pages. Rerun once to check no duplication.

**Exceptions and rollback:** Do not blindly retry an uncertain create. Look up the fixed username and employee ID, reconcile partial state and rerun the same approved snapshot.

**Evidence:** Approved source snapshot, change record, sanitized validation output, group screenshots and access tests.

## Move an employee

**Trigger:** Approved department transfer preserving identity. **Owner:** IAM operator, with HR/application-owner approval as applicable. **Manual:** Step 7.

**Prechecks:** Record current department and effective transfer; retain the prior approved source snapshot.

**Actions:** Change only department in employees.csv; dry-run; apply.

**Validation:** Old managed department absent, new department present in IdP and target; old portal resource denied and new one allowed.

**Exceptions and rollback:** Restore previous approved department only if rollback is authorized; do not keep both roles as an informal workaround.

**Evidence:** Before/after membership and resource tests, approved mover record and UTC completion time.

## Offboard an employee

**Trigger:** Authorized termination record. **Owner:** IAM operator, with HR/application-owner approval as applicable. **Manual:** Step 8.

**Prechecks:** Verify employee correlation and record all known applications, exceptional grants and tokens. Keep an existing app session for the test.

**Actions:** Set status=terminated; dry-run; apply. Review and revoke exceptional grants separately.

**Validation:** IdP disabled, target inactive, managed groups absent, fresh login blocked and existing protected portal access denied.

**Exceptions and rollback:** If downstream action fails, maintain containment and document partial state. Other applications and tokens need target-specific revocation checks.

**Evidence:** Leaver request, completed checks, exceptions/remaining actions and failed/successful reconciliation events.

## Reset an MFA authenticator

**Trigger:** Verified lost-device support request. **Owner:** IAM operator, with HR/application-owner approval as applicable. **Manual:** Step 8.

**Prechecks:** Verify identity through a pre-established independent process; log the method without recording sensitive verification material.

**Actions:** Remove the affected OTP credential in Keycloak, require Configure OTP, end appropriate IdP sessions and re-enrol the employee.

**Validation:** New authenticator works; previous OTP seed no longer works; fresh sign-in follows the intended flow.

**Exceptions and rollback:** Do not bypass recovery policy or weaken administrator protections. Escalate identity uncertainty.

**Evidence:** Support record, sanitized reset event metadata and recovery tests; no QR/seed screenshots.

## Recover failed provisioning

**Trigger:** Pipeline error or mismatched actual state. **Owner:** IAM operator, with HR/application-owner approval as applicable. **Manual:** Step 12.

**Prechecks:** Record affected employee and first failing boundary. Check IdP, target and approved source without changing multiple variables.

**Actions:** Correct the credential, connectivity or mapping issue; inspect uncertain writes; rerun the same approved snapshot.

**Validation:** Read both systems back and repeat employee positive/negative access tests before closure.

**Exceptions and rollback:** Do not assume a successful HTTP write means the whole workflow succeeded. Assign residual actions and use rollback where justified.

**Evidence:** Incident timeline, hypotheses, root cause, corrective change and verified retest.

## Standard command references

```powershell
# Validate proposed HR state without connecting or writing
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv
# Apply after reviewing the intended state
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv --apply
# Export current local target access and audit records
.\.venv\Scripts\python.exe automation\report.py
```

Dry-run validates input and intended state. It does not compare the current remote environment. The pipeline is a single-runner lab tool; do not run concurrent copies.
