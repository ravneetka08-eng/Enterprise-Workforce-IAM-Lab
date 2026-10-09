# Step 15 Add the optional Okta administration track

**Practical status: NOT STARTED.**


This track adds direct product experience where the free org exposes the required features. Keycloak remains your complete fallback. Do not claim Okta experience for modules you performed only in Keycloak. The free-plan feature list includes SSO, directory, adaptive MFA, lifecycle management, API access management and Workflows; full Okta Identity Governance is not listed [R2]. Do not activate a paid upgrade to follow this manual.

### Set up the directory and policies

1. Register an Integrator Free Plan at the official developer signup. Verify your tenant type and limits. Keep total active users, including administrators, within ten.
2. Preserve the original administrator and its enrolled recovery methods. Create up to three artificial employee accounts through Directory → People → Add person. Set activation/password options appropriate for a manual lab account; example.test addresses cannot receive real activation email.
3. Directory → Groups → Add group: create employees, dept-engineering, dept-finance and dept-hr. Assign the artificial users according to the role matrix.
4. Add profile attributes for employee ID and department using Directory → Profile Editor → Okta user profile. Choose string attributes and restrict who can modify authoritative fields. Record mappings and source ownership.
5. In Security → Authenticators inspect available password, Okta Verify and phishing resistant options. Configure an employee enrolment policy for the lab groups. Keep the only administrator out of experimental policies until recovery is verified.
6. In Security → Authentication Policies create an employee portal policy requiring available appropriate factors. In Global Session Policy configure and record a limited session lifetime. Test with a non-admin employee using a fresh browser session; existing session state can hide an intended challenge.
7. Simulate a verified MFA reset in Directory → People → employee → authenticator reset action. Re-enrol and capture sanitized System Log events. Exact labels vary by tenant engine/version; use the user profile's reset actions rather than looking for a factor in a different user's account.

### Connect the supplied OIDC portal to Okta

1. Applications → Applications → Create App Integration → OIDC → Web Application.
2. Name Northstar employee portal; select authorization code grant. Set sign-in redirect URI `http://localhost:5000/callback`. Assign only the approved lab employee groups. Do not select everyone for convenience.
3. Record the client ID and secret privately. Use the tenant's org authorization server discovery endpoint:

```text
https://YOUR-OKTA-DOMAIN/.well-known/openid-configuration
```

4. In app claims or authorization server claim configuration supported by your tenant, ensure the ID token provides `preferred_username` equal to the target userName. For an org authorization server this may require an application profile/claim mapping. The supplied portal intentionally refuses identity tokens missing this claim. If the tenant does not allow it, make a reviewed portal mapping change using a verified claim such as email only when its value is controlled, unique and identical to the synthetic username; do not silently fall back to arbitrary claims.
5. Stop Terminal A. Change OIDC_CLIENT_ID, OIDC_CLIENT_SECRET and OIDC_DISCOVERY to the Okta values; keep the existing SCIM token and portal secret. Restart the portal. Remove AUTHLIB_INSECURE_TRANSPORT if desired for the remote HTTPS IdP; local HTTP callbacks remain a development exception that the provider must support.
6. Provision matching synthetic usernames into the local target using the established lab pipeline or explicit SCIM requests. This target provisioning is still the local Python path, not native Okta provisioning. Sign into the portal via Okta and test allowed and denied access.
7. Unassign one disposable test user from the Okta app and test a fresh login. Separately deactivate the matching target account and test an existing app session. Record the different behaviours. Restore approved assignments afterward.
8. Before returning to the core labs, restore the workforce discovery URL and client credentials in Terminal A. Keep evidence labelled with the IdP used.

### Practise SAML with Okta as the IdP

1. Use the partner realm from Step 9 but add a separate SAML identity provider alias `okta-saml`. Copy its ACS and SP entity ID from the provider and its descriptor; do not overwrite workforce-saml.
2. In Okta create a SAML 2.0 application. Set Single sign-on URL to the partner provider ACS, Audience URI to its SP entity ID, Name ID format to EmailAddress and application username to the controlled synthetic username. Ensure response/assertion signatures are enabled as supported.
3. Assign only the lab employee group. Export IdP metadata from Okta's Sign On setup/instructions and import it into partner's okta-saml provider. Require signature validation and trust the metadata signing certificate.
4. In the partner account login choose the Okta provider. Complete sign-in and check partner's federated identity link and both systems' events. Existing auto-link policy must not let an unverified email take over an existing account.
5. Repeat the certificate mismatch and repair exercise, preserving administrator recovery access. Record this separately as an Okta SAML integration.

### Build an Okta Workflows exercise

1. Open Workflows from the admin console if available. Connect the Okta connector using the free org's supported authorization setup. Use only required permissions and record the integration owner.
2. Create a scheduled flow named Northstar joiner reconciliation. Add a Workflows table with employee_id, username, department, status and processed fields. Enter one synthetic joiner row.
3. Add table search for unprocessed rows and process each using a helper flow. Before creating a user, use the Okta connector to search or read the intended identity. If present, update the intended attributes rather than create another identity. Use employee_id as the correlation attribute.
4. For active rows, create/update the user and add the mapped department group. For movers, remove old managed department groups before adding the new group. For terminated rows, deactivate the test identity, remove assigned app access as required by connector behaviour and verify the intended target result before marking processed.
5. Add explicit error handling in the editor: leave processed false, record employee ID and error category in a failure table, and investigate before retry. Never record passwords or API tokens. Inspect actual connector card inputs/outputs because card names vary with connector version.
6. Keep the total including helper flows within the five-flow limit. Suggested allocation: one scheduler, one reconciliation helper, one error helper, one review export and one spare. Start with only the scheduler and reconciliation helper.
7. Test duplicate processing and a deliberately invalid group ID. Inspect execution history. Restore correct values and verify recovery. Mark processed only after a read-back of user status and expected group membership.
8. Export a sanitized flow diagram or capture card layout. Label this as a Workflows table acting as an HR source, not a production HRIS integration.

### Understand hosted SCIM limitations

Okta cannot connect to the local target at localhost. This manual deliberately avoids public tunnels and self-hosted public endpoints. You therefore have two separate pieces of evidence: local SCIM protocol implementation and, if eligible, Okta administration/integrations. Do not claim end-to-end Okta SCIM to this local target.

If an existing free supported application with accessible SCIM features is available to you later, onboard it using its documented endpoint, credentials and attribute mappings; test create, update, deactivate and separate app assignment from group push. Many SaaS products reserve SCIM for paid plans. Stop rather than upgrading when the exercise depends on such a plan. The supplied SCIM subset is not promised to be compatible with all native Okta Group Push operations.

**Governance boundary:** use Steps 10–11 for equivalent custom governance practice. If your free tenant lacks OIG, leave OIG as a learning gap. Do not call a Workflows access report an OIG certification campaign.
