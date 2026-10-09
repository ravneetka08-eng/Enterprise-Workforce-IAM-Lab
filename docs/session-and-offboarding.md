# Sessions and offboarding

The IdP session, app session, OAuth tokens and target account are separate access paths. Disabling sign-in may stop a new login without ending an already-created downstream session.

The local portal imposes a five-minute app session age and checks current target active status and membership on each protected request. Its logout clears the app session; it does not automatically log out Keycloak. lifecycle.py disables a leaver in Keycloak, requests IdP session logout and deactivates/removes managed access in the target.

Offboarding also requires exceptional grants, unrelated groups, other applications, token ownership and recovery/retention decisions. Prove both fresh-login denial and existing-session resource denial. Record any retained access as an explicit open action with owner and due date.

**Live behaviour and completion times: pending.**
