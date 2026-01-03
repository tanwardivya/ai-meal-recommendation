# Update IAM Policy for GitHub Actions Role

The IAM policy has been updated to include all necessary permissions. You need to update the existing policy.

## Quick Update

Run the setup script again to update the policy:

```bash
./setup-oidc-role.sh
```

This will update the existing policy with the new permissions.

## Manual Update

Or update the policy manually:

```bash
# Update the policy
aws iam create-policy-version \
  --policy-arn arn:aws:iam::928618160741:policy/github-actions-frontend-policy \
  --policy-document file://frontend-iam-policy.json \
  --set-as-default
```

## New Permissions Added

The updated policy now includes:

1. **ECR**: Full ECR access (CreateRepository, PutImage, etc.)
2. **IAM**: Create/Manage roles and policies for Elastic Beanstalk
3. **S3**: Create buckets for Elastic Beanstalk deployments
4. **Elastic Beanstalk**: Full management permissions
5. **EC2/Auto Scaling/ELB**: Full management for EB infrastructure
6. **CloudFormation**: For EB stack management
7. **CloudWatch Logs**: For EB logging

## Verify Policy

After updating, verify the policy:

```bash
aws iam get-policy-version \
  --policy-arn arn:aws:iam::928618160741:policy/github-actions-frontend-policy \
  --version-id $(aws iam get-policy --policy-arn arn:aws:iam::928618160741:policy/github-actions-frontend-policy --query 'Policy.DefaultVersionId' --output text)
```

