# Step 14 Operate the environment like an IAM service

**Practical status: NOT STARTED.**


### Define the operational runbooks

1. Create docs/runbooks.md with five procedures: onboard employee, move department, offboard employee, verified MFA reset and failed provisioning recovery. Each must have trigger, approved source, owner, prechecks, exact command or UI path, validation, exception handling and evidence.
2. Create docs/service-objectives.md with illustrative local objectives: scheduled onboarding ready before start; authorized urgent leaver action immediately upon receipt; failed reconciliation escalated before access is marked complete. State that actual corporate SLAs require business agreement, time coverage and tooling capacity.
3. Create docs/exception-register.csv with exception ID, identity, resource, reason, approver, start, expiry, compensating control, review owner and status. An exception without expiry is an unresolved risk, not a permanent workaround.
4. Create docs/risk-register.csv. Record broad automation permissions, local HTTP, operator-editable evidence, missing independently verified approver identity, absent commercial HRIS connector and no device compliance enforcement. For each record likelihood, impact, treatment, owner, validation and residual risk. Explain your scales; do not invent precision.

### Back up and recover

1. Stop the portal using Ctrl+C in Terminal A before copying its SQLite database, so you do not copy during a write. Copy `private/portal.db` to a dated file under private. Reopen the portal afterward with the same saved settings.
2. Stop Keycloak with `docker stop northstar-kc`. Use a local helper container to archive the named volume to a private host directory:

```powershell
$backupPath = (Resolve-Path private).Path
docker run --rm --mount 'type=volume,source=northstar-kc-data,target=/data,readonly' --mount "type=bind,source=$backupPath,target=/backup" alpine:3.22 tar czf /backup/keycloak-volume.tgz -C /data .
docker start northstar-kc
```

3. Treat the archive as secret-bearing identity data. Do not commit it. Keep the pinned image version recorded alongside it. A realm configuration export alone does not prove a full recovery of users, credentials and sessions.
4. For a restore rehearsal, keep the primary lab stopped. Restore the archive into a different new volume, create a separate container with the same image on loopback port 8081, and verify the realms and user records. Example:

```powershell
docker volume create northstar-kc-restore
docker run --rm --mount 'type=volume,source=northstar-kc-restore,target=/data' --mount "type=bind,source=$backupPath,target=/backup,readonly" alpine:3.22 tar xzf /backup/keycloak-volume.tgz -C /data
docker run -d --name northstar-kc-restore -p 127.0.0.1:8081:8080 -v northstar-kc-restore:/opt/keycloak/data quay.io/keycloak/keycloak:26.8.0 start-dev
```

5. Inspect `http://localhost:8081` privately. Stored localhost:8080 callbacks will not automatically match a moved environment; this test initially verifies directory recovery, not complete federation recovery. A complete recovery drill must deliberately adjust callbacks/issuer dependencies and retest the affected applications. Delete only the rehearsal container/volume when done and restart the primary.
6. Record backup time, restoration time, validation and limitations. A created backup file is not evidence that recovery works.

### Assess device trust honestly

Write a design exercise: managed device state would come from a trusted endpoint management system; the IdP would enforce device assurance or equivalent policies; recovery and exception paths would be defined. This project does not implement Jamf, Island, Google Workspace or Entra device compliance. Browser headers are not a trustworthy replacement for managed device posture.
