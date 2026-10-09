# Known limitations

- Three synthetic employee records model business roles; they do not demonstrate enterprise scale.
- The HR CSV emulates an authoritative source. No commercial HRIS connector is implemented.
- Usernames are fixed in this lab. Renames/rehires require an explicit correlation design.
- The target supports a documented SCIM subset, not every discovery/filter/PATCH/group-push operation.
- Keycloak Admin API and local SCIM are connected by Python; Keycloak is not represented as a native SCIM service.
- The pipeline is single-runner, with bounded retries and partial-state reconciliation rather than a distributed transaction or production queue.
- Authentication/session and provisioning state are separate. IdP logout does not universally revoke every issued token or SaaS session.
- Custom approval relies on operator-supplied reviewer identity; independent authenticated approval and tamper-resistant evidence are not implemented.
- Local activity shows only this portal. It is not comprehensive SaaS usage or shadow IT discovery.
- AWS results are policy simulation, not live S3 access or enterprise federation unless separately completed.
- Optional Okta work must be labelled separately. Full OIG, hosted SCIM compatibility, Jamf, Island, Google Workspace and Entra administration are not implied.
- Source preparation checks do not establish that your live Keycloak, AWS or Okta build works.

See the risk register for treatments and validation. This code must not be deployed directly as a corporate service.
