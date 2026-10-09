# Application source

portal.py implements the local employee portal, OIDC sign-in and a SCIM Users/Groups subset. Start it only after completing manual Step 4 credential and client configuration.

The server binds to loopback, uses development hosting and stores local state in private/portal.db. The target checks account activity, current memberships and unexpired grants on each protected request. This is learning code requiring further review and hardening before corporate use.
