# Step 7 Operate a mover and remove obsolete access

**Practical status: NOT STARTED.**


**What we are doing:** transfer Alex from Engineering to Finance. Giving the new access without removing old access creates privilege accumulation.

1. Save a copy of the original CSV as `data/employees-before-move.csv`.
2. Open a mover request in your change record: E001 transfers to Finance; effective immediately in the lab; manager approves; Engineering access is no longer justified.
3. In employees.csv change only Alex's department from engineering to finance. Keep E001 and username unchanged.
4. Run dry-run. Check that E001 now requires dept-finance. Run with `--apply` after checking the proposed state.
5. In Keycloak and SCIM Groups verify E001 is in employees and dept-finance, absent from dept-engineering.
6. Keep Alex's previously open portal session. Refresh Engineering: expect 403. Open Finance: expect 200. If five minutes elapsed, sign in again and repeat.
7. Read the existing OIDC session explanation: the portal uses current target membership at each protected request. This avoids trusting a stale department claim in an older token for its resource decisions.
8. Document the effective change time, old role removal, new role addition, tests and rollback. Rollback means restoring the approved previous department and reconciling; it is not simply adding both groups.

**Evidence:** before/after role matrix and HTTP results. **Checkpoint:** why can a mover still have a valid identity session while no longer being authorized for their old resource?
