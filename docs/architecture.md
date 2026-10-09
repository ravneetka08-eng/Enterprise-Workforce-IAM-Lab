# Identity architecture

**Status: proposed local design. Live connectivity pending validation.**

![Core architecture](architecture.png)

## Data flows

1. An approved HR CSV supplies immutable employee ID, fixed username, display names, department and employment status.
2. lifecycle.py validates the snapshot and calls Keycloak's Admin API with a service-account credential.
3. The same pipeline writes SCIM user and group resources to the local target and reads both systems back.
4. The portal uses an OIDC authorization-code flow and validates identity using Authlib.
5. The portal authorizes each protected request against current target account status, membership and temporary grants.
6. A partner realm accepts signed SAML authentication from the workforce realm.
7. Reports support business review and evidence collection; reports do not implement compliance automatically.

## Trust boundaries

| Boundary | Address or mechanism | Protection and limitation |
|---|---|---|
| Browser to Keycloak | localhost:8080 | Local HTTP development exception |
| Browser to portal | localhost:5000 | Local HTTP; signed application session |
| Automation to IdP | Admin API | Service-account bearer token; broad local realm user permissions |
| Automation to target | /scim/v2 | Shared random bearer token; documented subset |
| Approval operator to target | Local SQLite | Operator-controlled ledger; reviewer identity not independently verified |

## State ownership

HR owns employment status and department intent. Keycloak owns IdP credentials and sessions. The target owns provisioned accounts, memberships, local activity and temporary grants. The learner stores raw evidence privately and publishes sanitized examples.

## Production differences

Corporate operation would require HTTPS, hardened hosting, scoped administrative permissions, a secret store, a real authoritative HR integration, authenticated approval, independent durable logs, alerting and tested recovery. These are tracked as limitations rather than represented as implemented.
