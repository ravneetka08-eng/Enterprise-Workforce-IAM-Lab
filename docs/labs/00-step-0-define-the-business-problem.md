# Step 0 Define the business problem

**Practical status: NOT STARTED.**


**What we are doing:** translate the JD into access outcomes. In corporate work an IAM engineer starts with requirements, system owners and authoritative data, not a collection of users created without a purpose.

**Terms:** an identity is a representation of a person or workload. Authentication establishes who is signing in. Authorization decides what that identity may do. Provisioning creates or updates an account in a target system. Deprovisioning removes access; it does not always delete data. An identity provider, or IdP, authenticates users for other applications. An HRIS is a human resources information system that usually supplies employment status and organizational attributes.

1. Create `docs/scope.md` inside `iam-lab`.
2. Write the business problem: manual onboarding causes inconsistent access, department transfers leave old privileges, and leavers may retain application sessions.
3. Write the objective: reconcile approved HR records to IdP and portal access, prove removal, and document failures.
4. Name the scope: three artificial employees, one local portal, two identity realms for SAML, a local SCIM target and a manual approval ledger.
5. Name exclusions: production data, paid SaaS tenants, endpoint device compliance enforcement, commercial HRIS connectivity, enterprise high availability and regulated audit certification.
6. Assign simulated owners: HR owns employment status; department managers approve exceptional access; application owners define roles; IAM implements mappings; security reviews privileged access; an auditor reviews evidence. In this solo lab you act out these roles. This does not provide independently verified separation of duties.
7. Use `templates/change-record.md` to open CHG001 for the initial build. Document rollback as disabling the new client and restoring recorded settings, with database backup where necessary.

**Requirements to implement:** Engineering can access Engineering but not Finance; Finance can access Finance but not Engineering; movers lose the former department role; leavers cannot start new sessions and cannot use the portal through an existing session; temporary admin access expires; an inactive account is reviewed before deletion; failure is recorded instead of silently treated as success.

**Evidence:** scope document and first change record. **Checkpoint:** explain the difference between signing in successfully and being allowed to read Finance information.
