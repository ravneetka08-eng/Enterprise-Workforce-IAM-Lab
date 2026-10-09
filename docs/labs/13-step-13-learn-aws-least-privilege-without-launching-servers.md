# Step 13 Learn AWS least privilege without launching servers

**Practical status: NOT STARTED.**


**What we are doing:** author and test an identity policy for department-scoped read access. This is AWS IAM practice separate from workforce IdP administration. No bucket or EC2 instance is created, so this exercise does not incur infrastructure usage from those services.

**Terms:** ARN is an Amazon Resource Name. An identity policy is attached to a principal; a trust policy controls who may assume a role. Explicit deny overrides allow. If no applicable allow exists, the result is an implicit deny. The JSON Version 2012-10-17 selects the policy language version; it is not a certification that the policy is current or secure.

1. Sign into your existing AWS administrative identity with MFA. Open IAM → Policies → Create policy → JSON. Do not create a new root access key.
2. Paste this policy. The fictional bucket name represents a resource for simulation only:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListApprovedPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::northstar-iam-training-example",
      "Condition": {"StringLike": {"s3:prefix": ["engineering", "engineering/*"]}}
    },
    {
      "Sid": "ReadEngineeringObjects",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::northstar-iam-training-example/engineering/*"
    }
  ]
}
```

3. Inspect validation messages. Save as `NorthstarEngineeringReadLab` with a description explaining its simulation-only target. Do not attach it to your administrator.
4. Open IAM's current policy simulator feature from the IAM console. AWS moved the maintained simulator into IAM in July 2026 [R4]; old tutorials may show the standalone site.
5. Select a custom policy test if available and supply the policy. If the UI requires a principal, create a lab IAM user `northstar-policy-test` with no console password and no access keys, attach only this policy, and select it in the simulator. This user exists to evaluate policy; it is not your recommended production workforce identity pattern.
6. Run GetObject against `arn:aws:s3:::northstar-iam-training-example/engineering/handbook.txt`: expect allowed. Finance/handbook.txt: expect implicit deny. PutObject against Engineering: expect implicit deny.
7. Run ListBucket on the bucket ARN with s3:prefix set to engineering/: expect allowed. Repeat with finance/: expect implicit deny. The bucket ARN and object ARN are different; using the wrong ARN can invalidate the test.
8. Save the policy and simulation results to evidence. Label results as policy evaluation, not a successful live S3 request. The simulator does not create the bucket or prove all real-world access paths. Real access also depends on applicable resource policies, boundaries, organization controls and other context.
9. Delete the disposable principal after detaching the policy. Keep the policy until you finish the evidence, then delete it too.

**Optional existing-environment federation:** if you already have an appropriate IAM Identity Center organization instance and are willing to use it within your existing account setup, consult AWS's Okta SAML/SCIM integration guide [R5]. An account instance does not provide the same AWS account permission-set capabilities. This extension is not required for the free core and is not a reason to enable Organizations.

**Checkpoint:** explain why creating an IAM user with permanent access keys is not equivalent to federated workforce access using temporary role credentials.
