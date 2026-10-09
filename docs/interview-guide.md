# Interview explanation guide

Use this after completing the practical tests. Explain your own observations; do not present prepared documents as completed operational experience.

## Five minute demonstration

1. Describe the business problem and authoritative HR source.
2. Show Engineering allowed and Finance denied for the same identity.
3. Show a mover losing old access and gaining new access.
4. Show a leaver blocked using both a fresh login and existing application session.
5. Show temporary access expiring and a failed provisioning run being recovered.

## Questions to practise

- How are authentication, authorization and provisioning different?
- Why keep a stable employee identifier when each system has its own user ID?
- What happens if one system updates and the next request fails?
- Why is retrying an uncertain create risky?
- Why does IdP logout not universally revoke every application session/token?
- What prevents old department access accumulating?
- What does the custom approval ledger fail to verify?
- Which parts were Keycloak, which were Okta, and which were custom code?
- What additional controls would be needed in a corporate service?

## Resume statement after completion

Built a local workforce IAM lab with Keycloak OIDC and SAML federation, Python HR lifecycle reconciliation, a SCIM provisioning subset, expiring access grants and access-review reporting; validated joiner, mover and leaver outcomes.

Only add Okta or specific validated outcomes after completing those exercises. You need to understand the commands, dependencies and recovery path; memorizing every parameter is unnecessary.
