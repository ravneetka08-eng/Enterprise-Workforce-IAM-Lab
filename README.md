# Northstar Workforce IAM Lab

**Project status: implementation artefacts prepared; practical validation and publication sign-off not yet documented.**

This project develops workforce identity and access management skills using a local identity environment for a fictional company, Northstar People. It addresses inconsistent onboarding, obsolete access after transfers, delayed offboarding and poorly documented access decisions.

## Start the project

Read [START-HERE](START-HERE.md), then follow the [manual](IAM-Industry-Lab-Manual.docx) or its [browser version](docs/manual.html). The Markdown [manual](docs/manual.md) is also available. Commands run from this repository root.

## Implemented design and validation tracking

| Capability | Implementation | Validation status |
|---|---|---|
| Identity directory and groups | Keycloak workforce realm | Evidence not recorded |
| OIDC sign-in | Confidential portal client with code flow and PKCE | Evidence not recorded |
| SAML federation | Workforce IdP and partner broker realm | Evidence not recorded |
| Provisioning | Python bridge and a local SCIM HTTP subset | Evidence not recorded |
| Joiner mover leaver workflows | Approved HR snapshot reconciliation | Evidence not recorded |
| MFA support | OTP enrolment and verified recovery exercise | Evidence not recorded |
| Temporary access | Approval ledger with runtime expiry | Evidence not recorded |
| Access review | Target access and activity report with remediation | Evidence not recorded |
| AWS least privilege | Policy simulation without infrastructure | Evidence not recorded |
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

Record results in [test results](templates/test-results.csv), connect them to [evidence index](docs/evidence-index.csv), and update [progress](docs/progress.md). The repository includes implementation code and lab procedures. The supplied test-results ledger does not yet contain observed learner outcomes. Record real results and link evidence before claiming full practical completion. Code checks performed during preparation do not replace live integration tests.

See [known limitations](docs/known-limitations.md), [risk methodology](docs/risk-methodology.md) and [final report](docs/final-report.md). This is a learning portfolio, not a claim of production deployment or SOC 2/ISO 27001 compliance.

## Project completion and GitHub release gate

The source code and documentation are a project deliverable; the working identity environment and its validated outcomes are a separate deliverable. Before labelling this repository **Completed**, confirm the following:

1. Record actual outcomes for the core tests in `templates/test-results.csv`, including failed or blocked cases.
2. Link existing sanitized screenshots, logs, or command outputs in `docs/evidence-index.csv`; do not fabricate results or timestamps.
3. Finish access certification decisions, incident resolution, backup/restore observations, and residual-risk review.
4. Complete `docs/final-report.md` with observed results and explicitly identify untested features.
5. Inspect `git status` and `git diff --cached`, verify no secrets or raw identity databases are staged, then commit and push.
6. Verify the published README, links, images, and latest commit on GitHub.

**Scope note:** Optional Okta administration is not a prerequisite for core completion. This is an educational local lab, not a production IAM deployment or a compliance certification.
