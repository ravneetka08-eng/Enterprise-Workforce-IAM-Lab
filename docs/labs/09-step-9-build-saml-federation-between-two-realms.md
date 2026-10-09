# Step 9 Build SAML federation between two realms

**Practical status: NOT STARTED.**


**What we are doing:** configure a second application identity boundary using signed SAML assertions. The workforce realm is the IdP; a new partner realm is the SAML service provider through identity brokering. This is an actual local SAML exchange, not a diagram-only exercise. It is not a commercial SaaS integration.

**Terms:** an assertion is an IdP's signed statement about authentication and attributes. The Assertion Consumer Service, or ACS, receives the response. An entity ID identifies a SAML party. Metadata distributes endpoints and public signing certificates. A certificate rollover changes trusted keys and needs coordination. SAML signing certificates are different from HTTPS server certificates.

1. In the realm selector create `partner`. Keep registration off. Enable login/admin events as you did in workforce.
2. In partner → Identity providers → Add provider → SAML v2.0. Alias: `workforce-saml`. Display name: Workforce SAML.
3. In its import configuration use the workforce metadata URL:

```text
http://localhost:8080/realms/workforce/protocol/saml/descriptor
```

Select Import if shown, review the endpoints, enable Validate signature, and save. Keep signed assertions required. If a signing certificate is not populated, inspect the metadata's signing KeyDescriptor and import its X509Certificate into the validating certificate field. Public certificates can be shared; private keys cannot.

4. In the provider configuration copy the Redirect URI shown by Keycloak. It should be `http://localhost:8080/realms/partner/broker/workforce-saml/endpoint`. This is the ACS we need on the workforce client.
5. Set Service provider entity ID, if exposed, to `http://localhost:8080/realms/partner`. Record its exact value. Open the provider's SAML SP metadata endpoint:

```text
http://localhost:8080/realms/partner/broker/workforce-saml/endpoint/descriptor
```

6. Switch to workforce → Clients → Import client. Import the partner SP metadata XML by pasting its contents or saving and choosing it. This preserves compatible entity ID, ACS and signing configuration. If the import UI is absent, create a SAML client with Client ID equal to the SP entity ID and the ACS from action 4, then copy the metadata's certificates and settings deliberately.
7. In the SAML client verify Force POST binding is on, Sign assertions is on and Name ID format is username. Ensure signing settings match the imported metadata. If Client signature required is on, the partner provider must sign its requests and the workforce client must trust the partner's public key. Use metadata rather than turning signature validation off to hide an error.
8. Open `http://localhost:8080/realms/partner/account` in a new private window. Select Workforce SAML on the login screen. Sign in as Alex at workforce, including MFA. On first broker login complete the Review profile screen and supply artificial profile values if required. Do not auto-link an account just because an unverified email matches.
9. Verify a brokered Alex account appears in partner → Users → Federated identities with provider workforce-saml. Verify the workforce login event and the partner broker event. Partner access does not automatically inherit all workforce portal authorization; each application owns its entitlements.
10. Open browser Developer Tools → Network before logging in again. Observe the ACS POST and SAMLResponse field. Do not publish the raw assertion: it contains identity/session data. Capture only sanitized endpoint names and a note that signature validation was enabled.
11. Negative test: temporarily set the validating certificate to an unrelated public certificate in partner, using a recorded change. New SAML sign-in should fail. Restore the trusted metadata/certificate and retest. Keep recovery access through the master admin console.
12. Explain a planned rollover: import the new trusted key before changing the IdP signer, maintain overlap where supported, test in a non-production environment, monitor failures, and retire the old key after the agreed overlap period.

**Evidence:** both realm settings, metadata trust relationship, successful brokered login, failed wrong-certificate test and restoration. **Checkpoint:** do not call a base64-decoded assertion verified until the signature, issuer, audience, destination and time conditions have been validated.
