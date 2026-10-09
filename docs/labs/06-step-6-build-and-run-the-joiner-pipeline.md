# Step 6 Build and run the joiner pipeline

**Practical status: NOT STARTED.**


**What we are doing:** provision employees from approved HR records. This is a complete local pipeline rather than an instruction to manually create users and call it automation.

1. In workforce → Clients → Create client, select OpenID Connect; client ID `hr-automation`.
2. Enable Client authentication and Service accounts roles. Disable Standard flow, Direct access grants and Implicit flow. Save.
3. Open Service account roles → Assign role. Filter by clients; select realm-management. Assign `manage-users`, `view-users`, `query-users` and `view-realm`. Do not assign realm-admin. Record that manage-users is still broad in this disposable realm; production should use finer scoped permissions where possible.
4. Copy the client secret from Credentials privately.
5. In Terminal B set:

```powershell
$env:KC_AUTOMATION_SECRET = Read-Host 'Paste the hr automation client secret'
$env:KC_BASE = 'http://localhost:8080'
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv
```

6. Expect a printed desired state for E001, E002 and E003, followed by DRY RUN. This validates CSV format and proposed state, not the current remote environment. No credentials are used until `--apply`.
7. Open `data/employees.csv`. Understand every field: employee_id stays stable; username is fixed in this lab; first_name and last_name are display data; department selects managed access; status is active or terminated. Only artificial `@example.test` identities are accepted.
8. Record the approved joiner change. Then execute:

```powershell
.\.venv\Scripts\python.exe automation\lifecycle.py data\employees.csv --apply
```

9. Expect `VALIDATED E001`, `VALIDATED E002`, `VALIDATED E003`. In Keycloak → Users verify three users, enabled status, employeeId and the expected groups. Inspect the SCIM target using Step 5.
10. In each Keycloak employee's Credentials tab choose Set password. Use a different strong local lab password and set Temporary on so the employee must change it at first login. The script deliberately does not create, email or log passwords.
11. Open a private browser window and sign into the portal as Alex. Change the temporary password if requested. Home should display employees and dept-engineering. Engineering should return 200; Finance should return 403. Repeat with Priya and Lee. HR should not receive either department resource.
12. Run the same apply command again. Confirm no additional users or groups appear and membership is unchanged. This is idempotency: applying the same intended state should not duplicate identities.

**Script behaviour:** it validates input before writes, correlates employee IDs, creates missing active identities, updates approved managed groups, provisions target accounts, reads both systems back and logs success only after state validation. It does not delete a person just because they are absent from the CSV. Absence is ambiguous; terminated is an explicit instruction. It manages four groups and leaves other groups alone.

**Failure boundary:** reconciliation is not an atomic transaction across systems. A later failure can leave earlier changes applied. The script stops with a failure record. Read the affected identity in both systems, repair the cause and rerun the same approved snapshot. It retries limited HTTP 429 and server errors with backoff; it stops on connection uncertainty. Never blindly replay an uncertain create—look for the existing identity first. It is single-runner tooling; do not execute concurrent copies.

**Evidence:** approved snapshot, sanitized successful run, Keycloak group membership, target account, allowed/denied tests and rerun count. **Checkpoint:** distinguish a real vendor HRIS connector from a CSV that emulates the authoritative HR source.
