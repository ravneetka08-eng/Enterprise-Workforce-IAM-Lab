# Project scope

**Document status: planned design. Implementation and observed outcomes pending.**

## Business problem

Manual employee onboarding can create inconsistent access. Department transfers can leave obsolete privileges, and terminated employees can retain downstream accounts or application sessions. Reviewers need reliable evidence connecting each access change to an approved business requirement.

## Objective

Reconcile approved artificial HR records to identity-provider and portal access, verify joiner/mover/leaver outcomes, handle errors explicitly and maintain reviewable change evidence.

## In scope

- Three artificial employee identities for Engineering, Finance and HR.
- A Keycloak workforce realm with groups, session settings, MFA and administrative event capture.
- A local OIDC employee portal and partner realm for SAML federation.
- Python lifecycle automation and a local SCIM provisioning subset.
- Expiring privileged-access approval, access certification and inactivity review.
- AWS policy authoring and simulation without running infrastructure.
- An optional Okta free-tenant exercise where eligibility permits.

## Out of scope

Production identities/data, paid SaaS tenants, commercial HRIS integration, verified independent approval, enterprise availability, native complete Okta SCIM, managed-device compliance and audit certification.

## Responsibility model

| Simulated role | Responsibility |
|---|---|
| HR | Employment status and approved department data |
| Department manager | Business justification and exceptional access approval |
| Application owner | Application role definitions and review decisions |
| IAM operator | Configuration, reconciliation and validation |
| Security reviewer | Privileged access and incident review |
| Evidence reviewer | Traceability and completeness of records |

One learner role-plays these responsibilities. This is not enforced independent separation of duties.

## Acceptance

Positive and negative RBAC tests; duplicate rerun; department move; new-session and existing-session leaver tests; MFA recovery; SAML trust failure; expiry and self-approval rejection; access-review remediation; failed provisioning recovery; labelled AWS simulation; sanitized evidence and cleanup.
