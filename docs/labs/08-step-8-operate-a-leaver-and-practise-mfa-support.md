# Step 8 Operate a leaver and practise MFA support

**Practical status: NOT STARTED.**


### Remove employee access

1. Keep Priya logged into the Finance resource in a private window.
2. Create an authorized leaver record for E002. State the lab target: block new sign-in and protected portal access after completed reconciliation. In production the required timing comes from risk, HR process and contracts.
3. Set Priya's status to terminated in employees.csv; do not delete the row. Run dry-run and apply.
4. Check Keycloak enabled is false and managed group memberships are gone. The script disables the IdP before downstream cleanup and requests Keycloak session logout.
5. Check target `active` is false and managed groups are gone.
6. Refresh Priya's existing portal Finance page. Expect 403 even if the local app cookie has not expired. Open a fresh private window and attempt IdP sign-in: it should fail.
7. Export evidence and retain the account record. Deactivation and deletion are separate decisions; employee documents or ownership may need retention and transfer.
8. Run `automation/report.py` in Step 11 and look for any still-live temporary grants. Active-check enforcement prevents a disabled user using them, but clean up the ledger too. Offboarding is not complete until exceptional grants, tokens and other applications are reviewed.

**Important:** ending an IdP session does not universally revoke every issued access token, every SaaS session or every application cookie. This portal rejects deactivated accounts through its own live check. A production leaver plan must include target-specific session and token behaviour, revocation capabilities, service ownership and credential rotation.

### Enrol and recover MFA

**Terms:** MFA combines factors from distinct categories, such as a password and a possession factor. TOTP is a time-based one-time password. TOTP improves on password-only login but is not phishing resistant. WebAuthn/passkeys or security keys may provide phishing resistant authentication.

1. In workforce → Authentication → Required actions enable Configure OTP. In Users → Alex → Details add Configure OTP to Required user actions; save. Do the same for each active employee. The supplied script preserves existing user settings rather than defining these required actions.
2. Open Authentication → Flows → browser and inspect the OTP step. Ensure the standard browser flow's conditional OTP path is enabled so configured OTP is requested. Do not replace the flow without a separate change plan.
3. Sign Alex out of Keycloak using its Account Console Sessions page or administrator session logout, then open a new private window. Sign in, scan the OTP setup code with a free authenticator app and supply the code. Never save the QR code or shared seed as evidence.
4. Sign out and sign in again. Expect an OTP challenge. Test one wrong code and one correct code; record outcomes. If no OTP is requested, investigate the bound browser flow and saved credentials.
5. Simulate a lost phone with a help desk ticket. Verify the employee using a pre-established independent process, such as a callback to an already recorded number and manager confirmation. Do not rely only on an email from the person requesting the reset. In the lab this verification is role-played and documented.
6. In Users → Alex → Credentials remove the OTP credential, add Configure OTP as a required action, and end current IdP sessions. Re-enrol using a new secret.
7. Verify the new OTP works and the former seed no longer generates valid codes for this account. Capture credential reset event metadata, never the credential values.
8. Record the support ticket, verification method, administrator action, session handling and successful recovery. Discuss how phishing resistant authenticators and recovery policy would change the design.

**Checkpoint:** why is an MFA reset itself a sensitive privileged operation?
