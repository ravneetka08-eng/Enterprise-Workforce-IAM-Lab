# Step 10 Implement temporary access requests and expiry

**Practical status: NOT STARTED.**


**What we are doing:** add an approval-controlled entitlement with automatic runtime expiry. A ticket saying approved is insufficient unless something enforces the decision.

The supplied governance command reads requests, rejects self-approval, checks a reviewer allowlist, allows only portal-admin and limits new grants to at most one hour. It stores the expiry in the target database. The portal checks the grant and active account on every admin request. Reviewer identity is supplied in a local CSV by the operator; it is not independently authenticated. A corporate version needs an authenticated request interface, verified approver identity, resource owner rules, tamper-resistant history and service boundaries.

1. Restore Alex to active if you previously terminated Alex. Priya can remain terminated.
2. Open `data/requests.csv`. Keep request_id REQ001, username Alex, entitlement portal-admin and reviewer manager.engineering@example.test. Write a meaningful business justification.
3. Generate an expiry five minutes in the future:

```powershell
.\.venv\Scripts\python.exe -c "import time; print(int(time.time()+300))"
```

4. Replace REPLACE_WITH_FUTURE_EPOCH in requests.csv with that number. Unix epoch is seconds since 1 January 1970 UTC. Generate it immediately before the test.
5. Before applying the request, Alex's `/admin` page should return 403. Run:

```powershell
.\.venv\Scripts\python.exe automation\governance.py data\requests.csv
.\.venv\Scripts\python.exe automation\governance.py data\requests.csv --apply
```

6. Expect Alex's `/admin` page to return 200 after approval. After expiry it must return 403, without any manual group removal. If the five-minute local session expires, sign in again and verify the grant is still denied.
7. Test self-approval using a copy of requests.csv with reviewer equal to Alex. The command must reject it; no new grant should appear.
8. Test an unknown reviewer, missing justification and expiry more than an hour away. Each must fail. Use different request IDs for genuinely different requests; reusing REQ001 with changed values is rejected.
9. Revoke a valid unexpired request by setting decision to revoke and running apply. Record the original request, approval, enforcement result and revocation. Do not edit historical evidence to pretend the earlier access never existed.

**Evidence:** sanitized request ledger, pre-approval denial, approved access, expiry denial and negative tests. **Checkpoint:** distinguish operational expiry enforcement from a scheduler that merely emails someone when access should end.
