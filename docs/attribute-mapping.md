# Attribute and group mappings

| HR field | IdP field | Target field | Ownership rule |
|---|---|---|---|
| employee_id | attributes.employeeId | externalId | Stable HR correlation; do not reuse |
| username | username | userName | Fixed and unique in this lab |
| first_name | firstName | name.givenName | HR-owned display attribute |
| last_name | lastName | name.familyName | HR-owned display attribute |
| department | Managed group choice | Managed group membership | Approved HR department |
| status | enabled | active | Explicit active or terminated value |

The IdP user ID and target user ID are generated independently. Do not confuse them with the HR employee ID. A conflicting stored employee ID requires manual investigation. Name or username changes need a separate design because this lab correlates lookups using fixed usernames.

Only employees, dept-engineering, dept-finance and dept-hr are managed by lifecycle.py. Other access must be independently inventoried and reviewed, especially during offboarding.
