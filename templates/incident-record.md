# Identity incident record
Incident ID and UTC time: 0001 and 13/10/26,10:20pm
Reporter and verified identity method: OIDC Redirect URI Mismatch
Symptom and affected application: employee portal
Business impact and priority: SSO failure
Evidence with correlation identifiers: events from workforce realm in keycloak
Hypotheses and checks: done
Containment: done
Root cause: wrong callback address
Corrective action: correct callback address
Retest results: no need
Communication: done
Prevention and closure owner: settled
Before deploying OIDC client configuration changes, validate the application's callback URL against Keycloak's approved redirect URI list. Test authentication after the change and maintain a documented rollback procedure.
