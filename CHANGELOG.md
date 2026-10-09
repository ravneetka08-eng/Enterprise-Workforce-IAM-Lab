# Changelog

## Initial prepared repository

Added the manual, application and automation source, artificial inputs, design documentation, operational runbooks, change plans, registers, lab guides and evidence folders. Live learner validation remains pending.


## Change: Initial Workforce Joiner Provisioning

- **Type:** Joiner
- **Employees:** E001 Alex, E002 Priya, E003 Lee
- **Change:** Provisioned active workforce identities from the approved HR CSV.
- **Access:** Assigned baseline `employees` group and appropriate department groups.
- **Validation:** Keycloak and SCIM accounts validated; allowed/denied portal access tested successfully.
- **Result:** Successful.

## Change: E001 Engineering to Finance

- **Type:** Mover
- **Employee:** E001 Alex
- **Change:** Transfer from Engineering to Finance.
- **Approval:** Manager approved; effective immediately in lab.
- **Required Access:** Remove `dept-engineering`, add `dept-finance`, retain `employees`.
- **Reason:** Engineering access is no longer justified after the transfer.
- **Status:** Approved / Pending implementation.


## Change: E002 Employee Termination

- **Type:** Leaver
- **Employee:** E002 Priya
- **Approval:** Authorized leaver request
- **Effective:** Immediately in lab
- **Required Action:** Disable identity and remove managed access
- **Target:** Block new sign-in and protected portal access after reconciliation
- **Status:** Approved / Pending implementation


## MFA Recovery — E001 Alex

- **Issue:** Lost MFA device
- **Identity Verification:** Recorded-number callback + manager confirmation (lab simulation)
- **Admin Action:** Removed old OTP credential
- **Required Action:** Configure OTP added
- **Sessions:** Existing IdP sessions terminated
- **Recovery:** New OTP credential enrolled
- **Validation:** New OTP accepted; former OTP no longer valid
- **Result:** Successful