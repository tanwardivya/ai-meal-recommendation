# OIDC Setup for Frontend Deployment

This guide explains how to set up OIDC (OpenID Connect) authentication for GitHub Actions to deploy the frontend application to AWS Elastic Beanstalk.

## Quick Setup

Run the setup script:

```bash
./setup-oidc-role.sh
```

This will:
1. Check/create OIDC provider
2. Create IAM policy with necessary permissions
3. Create IAM role with OIDC trust policy
4. Attach policy to role
5. Output the role ARN for GitHub Secrets

## Manual Setup

### Step 1: Get GitHub OIDC Thumbprint

```bash
echo | openssl s_client -servername token.actions.githubusercontent.com \
  -showcerts -connect token.actions.githubusercontent.com:443 2>/dev/null | \
  openssl x509 -fingerprint -noout -sha1 | \
  sed 's/://g' | \
  cut -d'=' -f2 | \
  tr '[:upper:]' '[:lower:]'
```

### Step 2: Create OIDC Provider (if not exists)

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list <THUMBPRINT_FROM_STEP_1>
```

### Step 3: Create IAM Policy

```bash
aws iam create-policy \
  --policy-name github-actions-frontend-policy \
  --policy-document file://frontend-iam-policy.json \
  --description "Policy for GitHub Actions to deploy frontend to Elastic Beanstalk"
```

### Step 4: Create IAM Role

```bash
aws iam create-role \
  --role-name github-actions-frontend-role \
  --assume-role-policy-document file://github-actions-trust-policy.json \
  --description "IAM role for GitHub Actions to deploy frontend application"
```

### Step 5: Attach Policy to Role

```bash
aws iam attach-role-policy \
  --role-name github-actions-frontend-role \
  --policy-arn arn:aws:iam::928618160741:policy/github-actions-frontend-policy
```

### Step 6: Get Role ARN

```bash
aws iam get-role --role-name github-actions-frontend-role --query 'Role.Arn' --output text
```

## Add to GitHub Secrets

1. Go to your GitHub repository: `tanwardivya/ai-meal-recommendation`
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add the following secrets:

   - **Name**: `AWS_ROLE_ARN`
   - **Value**: `arn:aws:iam::928618160741:role/github-actions-frontend-role`

   (Optional) For separate test/prod roles:
   - **Name**: `AWS_TEST_ROLE_ARN`
   - **Value**: `arn:aws:iam::928618160741:role/github-actions-frontend-role`
   
   - **Name**: `AWS_PROD_ROLE_ARN`
   - **Value**: `arn:aws:iam::928618160741:role/github-actions-frontend-role`

## Permissions Included

The IAM policy (`frontend-iam-policy.json`) includes permissions for:

- **Pulumi**: Full access to manage infrastructure
- **ECR**: Push/pull Docker images
- **Elastic Beanstalk**: Full management of applications and environments
- **S3**: Create buckets and upload deployment bundles
- **IAM**: Pass roles to Elastic Beanstalk (for service roles and instance profiles)
- **EC2/ELB/Auto Scaling**: Read-only for monitoring

## Security

The trust policy is restricted to:
- Repository: `tanwardivya/ai-meal-recommendation`
- Service: `sts.amazonaws.com` (AWS Security Token Service)
- OIDC Provider: GitHub Actions

This ensures only workflows from this repository can assume the role.

## Troubleshooting

### Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

1. Check OIDC provider exists:
   ```bash
   aws iam list-open-id-connect-providers
   ```

2. Verify trust policy matches repository:
   ```bash
   aws iam get-role --role-name github-actions-frontend-role --query 'Role.AssumeRolePolicyDocument'
   ```

3. Check GitHub repository name matches trust policy

### Error: "Access Denied" when deploying

1. Verify policy is attached:
   ```bash
   aws iam list-attached-role-policies --role-name github-actions-frontend-role
   ```

2. Check policy permissions include required actions

3. Verify role ARN in GitHub Secrets is correct

