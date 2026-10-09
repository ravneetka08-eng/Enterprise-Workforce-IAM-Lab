# Role and entitlement matrix

**Status: approved lab design assumption; actual assignments pending.**

| Identity | HR ID | Department | Managed groups | Engineering | Finance |
|---|---|---|---|---|---|
| alex.engineer@example.test | E001 | Engineering | employees; dept-engineering | Allow | Deny |
| priya.finance@example.test | E002 | Finance | employees; dept-finance | Deny | Allow |
| lee.hr@example.test | E003 | HR | employees; dept-hr | Deny | Deny |

A mover receives employees plus the new department group and loses the previous managed department group. A leaver is disabled and loses all managed groups. Groups outside the pipeline's managed set require separate review.

Temporary portal-admin is evaluated from an expiring target grant, not automatic department membership. No employee is entitled to Keycloak administrative privileges. hr-automation uses service credentials rather than an employee login.
