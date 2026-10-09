# Step 5 Inspect the provisioning API before automating it

**Practical status: NOT STARTED.**


**What we are doing:** examine real HTTP provisioning requests and understand their effects. SCIM is the System for Cross-domain Identity Management. SSO answers who the user is; SCIM maintains accounts and memberships in the target.

The supplied target implements Users and Groups with creation, retrieval, replacement, deletion, simple equality filters, pagination and a limited replace PATCH. It uses SQLite for persistence and enforces a shared bearer token. It does not implement full SCIM discovery, bulk operations, full filter grammar, ETags or every PATCH path. Do not describe it as a certified connector. Keycloak core is not being used as a native SCIM server; Python bridges its Admin API and this SCIM target.

1. Open Terminal B. Use the same SCIM token from Terminal A:

```powershell
$env:SCIM_TOKEN = Read-Host 'Paste the saved local SCIM token'
$headers = @{Authorization = "Bearer $env:SCIM_TOKEN"}
Invoke-RestMethod -Uri 'http://localhost:5000/scim/v2/Users' -Headers $headers
```

2. Expect a SCIM ListResponse, initially with `totalResults` zero. Save a sanitized response in your evidence notes. Do not copy headers containing the bearer token.
3. Test an incorrect credential:

```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/scim/v2/Users' -Headers @{Authorization='Bearer deliberately-wrong'}
```

Expect HTTP 401; PowerShell presents this as an error. This is a passing negative test.

4. Leave target user creation to the lifecycle script. After Step 6, return and retrieve an account using a userName filter:

```powershell
$filter = [uri]::EscapeDataString('userName eq "alex.engineer@example.test"')
$u = Invoke-RestMethod -Uri "http://localhost:5000/scim/v2/Users?filter=$filter" -Headers $headers
$u.Resources
```

5. Inspect `id`, `externalId`, `userName`, `name` and `active`. The target's id is its internal identifier. externalId is E001, the HR correlation identifier. They are not interchangeable.
6. After saving your normal joiner evidence, use this explicit deactivation request for a later negative test:

```powershell
$id = $u.Resources[0].id
$body = @{schemas=@('urn:ietf:params:scim:api:messages:2.0:PatchOp'); Operations=@(@{op='replace'; path='active'; value=$false})} | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Patch -Uri "http://localhost:5000/scim/v2/Users/$id" -Headers $headers -ContentType 'application/scim+json' -Body $body
```

Do not deactivate E001 until you have tested normal access. Reapply the approved active HR snapshot in Step 6 to restore it. Record the deviation and reconciliation.

**Checkpoint:** explain HTTP 200, 201, 204, 400, 401, 403, 404, 409 and 429. A 401 is an invalid or missing credential; a 403 generally means the request is recognized but forbidden. A 409 duplicate requires reconciliation, not blindly retrying creation.
