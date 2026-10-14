# Final project report

**Release status: NOT YET SIGNED OFF — implementation present, practical results not fully recorded.**

## Objective and environment

Develop workforce IAM engineering skills using a fictional Northstar People environment with Keycloak, a Flask employee portal, Python HR reconciliation, a local SCIM subset, SAML/OIDC and custom governance tooling. AWS policy simulation is a separate learning exercise; Okta is optional.

## Implementation artefacts present in the repository

- Portal and local SCIM target source code under `app/`.
- Lifecycle, governance and reporting scripts under `automation/`.
- Synthetic HR and request inputs under `data/`.
- Architecture, IAM controls, runbooks, service objectives, risk and exception registers under `docs/`.
- Manual, lab instructions, test template and evidence folder structure.

**These are file-level findings, not proof that every live integration or exercise passed.**

## Practical outcomes and evidence

| Area | Current documented result | Sign-off requirement |
|---|---|---|
| OIDC and RBAC | Not independently recorded | Successful SSO and allowed/denied resource tests |
| SCIM and joiner/mover/leaver | Not independently recorded | Read-back, session-denial and idempotency results |
| MFA and SAML | Not independently recorded | Positive and negative sign-in tests |
| Temporary access governance | Not independently recorded | Approval rejection, grant expiry and revocation |
| Access certification | Decisions/remediation require confirmation | Owner decision and verified before/after state |
| Incident handling | Incident worksheet exists; closure not established | Root cause, recovery, retest and evidence |
| AWS IAM | Simulation outcome not independently recorded | Policy JSON and observed allowed/denied simulations |
| Backup/restore | Not independently recorded | Restore rehearsal observations and limitations |
| Costs and cleanup | Not independently recorded | Actual cost check and retained-resource statement |
| Optional Okta | Not claimed | Document as N/A unless actually performed |

Use `templates/test-results.csv` for observed outcomes and `docs/evidence-index.csv` to link sanitized proof. No test should be marked PASS solely because its expected result is described in the manual.

## Known limitations and residual risk

The HR source is a CSV, not a commercial HRIS; the SCIM target supports a subset of the standard; approvals are not independently authenticated; evidence can be modified by a local operator; development services use loopback HTTP; device compliance and enterprise availability are not implemented. Review `docs/risk-register.csv`, `docs/risk-methodology.md` and `docs/known-limitations.md` before release.

## Final release checklist

- [ ] Actual test outcomes entered and cross-referenced to available evidence.
- [ ] Access-review findings and exception/risk owners reviewed.
- [ ] Incident and recovery outcomes recorded, or limitations explicitly disclosed.
- [ ] Final observed costs and cleanup/retention recorded.
- [ ] Public files checked for secrets and sensitive local data.
- [ ] Git changes reviewed, committed and pushed; remote repository verified.

**Completion decision:** Pending the above checks. This report intentionally does not invent evidence or represent the lab as a production deployment or audited control environment.
