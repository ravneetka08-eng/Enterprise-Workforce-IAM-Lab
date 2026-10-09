# Northstar Workforce IAM Lab

**Project status: prepared for implementation. Practical validation is pending.**

This project develops workforce identity and access management skills using a local identity environment for a fictional company, Northstar People. It addresses inconsistent onboarding, obsolete access after transfers, delayed offboarding and poorly documented access decisions.

## Start the project

Read [START-HERE](START-HERE.md), then follow the [manual](IAM-Industry-Lab-Manual.docx) or its [browser version](docs/manual.html). The Markdown [manual](docs/manual.md) is also available. Commands run from this repository root.

## Planned capabilities

| Capability | Implementation | Validation status |
|---|---|---|
| Identity directory and groups | Keycloak workforce realm | Pending |
| OIDC sign-in | Confidential portal client with code flow and PKCE | Pending |
| SAML federation | Workforce IdP and partner broker realm | Pending |
| Provisioning | Python bridge and a local SCIM HTTP subset | Pending |
| Joiner mover leaver workflows | Approved HR snapshot reconciliation | Pending |
| MFA support | OTP enrolment and verified recovery exercise | Pending |
| Temporary access | Approval ledger with runtime expiry | Pending |
| Access review | Target access and activity report with remediation | Pending |
| AWS least privilege | Policy simulation without infrastructure | Pending |
| Okta administration | Optional eligible free-tenant track | Not started |

![Architecture](docs/architecture.png)

## Repository navigation

| Location | Contents |
|---|---|
| [docs](docs/README.md) | Requirements, design, controls, runbooks, registers and reports |
| [app](app/README.md) | Employee portal and SCIM target |
| [automation](automation/README.md) | Lifecycle, approval and reporting scripts |
| [data](data/README.md) | Artificial HR records and sample access request |
| [templates](templates/README.md) | Reusable change, incident and test records |
| [evidence](evidence/README.md) | Sanitized evidence folders for each practical step |
| private | Local credentials, database, raw exports and backups; excluded from Git |

## Role model

Engineering employees receive Engineering access; Finance employees receive Finance access. HR receives neither protected department resource. Temporary portal administration requires a separately approved unexpired grant. Employee identities receive no realm administration privileges.

## Scope and limits

The project uses real local protocol requests with artificial identities. The CSV emulates an HR source; the SCIM server implements a subset rather than a certified connector; the approval ledger does not authenticate an independent approver. Keycloak and the portal use development hosting on loopback only. Device compliance, commercial HRIS connectivity and paid OIG are outside the core.

The core needs no paid services or running AWS compute. See [cost register](docs/cost-register.md). Do not enable Organizations to follow the core project. Optional Okta depends on signup eligibility and available free features.

## Evidence and progress

Record results in [test results](templates/test-results.csv), connect them to [evidence index](docs/evidence-index.csv), and update [progress](docs/progress.md). No learner test has been marked passed in this starter. Code checks performed during preparation do not replace your live integration tests.

See [known limitations](docs/known-limitations.md), [risk methodology](docs/risk-methodology.md) and [final report](docs/final-report.md). This is a learning portfolio, not a claim of production deployment or SOC 2/ISO 27001 compliance.
