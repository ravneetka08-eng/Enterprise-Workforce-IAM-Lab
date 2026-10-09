# Access policy

**Policy status: educational lab design. Enforcement tests pending.**

## Standard access

An active employee receives only the application role associated with an approved department. The target account must be provisioned and active. Successful authentication is necessary but does not automatically authorize a protected resource.

## Privileged access

portal-admin requires a request ID, identified employee, business justification, allowed reviewer, explicit approval and an expiry within the next hour. The portal checks expiry at request time. Self-approval is rejected by the command. Reviewer identity in the CSV is a role-played input rather than an authenticated independent decision.

## Movers and leavers

A department move removes previous managed department access. A terminated employee is disabled in the IdP before downstream cleanup, removed from managed groups and denied protected portal access. Exceptional grants and other application/session/token paths must also be reviewed.

## Recovery

MFA reset requires a pre-established independent verification method and a support record. New authenticator enrolment and session handling must be validated. Do not retain QR codes, seeds, passwords or token values in public evidence.

## Reviews and exceptions

Resource owners review actual access against current employment and business need. Every exception needs an owner, justification, approver and expiry. Unresolved items remain open with a due date; an exported report is not equivalent to completed certification.
