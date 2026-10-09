# Backup and recovery plan

Follow Step 14 of the manual for exact volume archive/restore commands.

1. Stop portal writes before copying private/portal.db.
2. Stop Keycloak before archiving the northstar-kc-data volume.
3. Store secret-bearing backups privately with image/version details.
4. Restore into a separate rehearsal volume and loopback port while avoiding interference with the primary lab.
5. Verify realms/users and then address callback/issuer dependencies before claiming full application recovery.
6. Record actual elapsed time and validated recovery scope.
7. Remove only the rehearsal resources after capturing sanitized evidence.

A file that exists is not evidence of recoverability. A realm configuration export alone does not prove recovery of users, credentials and sessions.

**Backup date, restore time and validation outcomes: pending.**
