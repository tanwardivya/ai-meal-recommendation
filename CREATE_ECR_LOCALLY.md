# Create ECR Repository Locally

## Step 1: Create ECR Repository

Run this command locally (from your machine):

```bash
aws ecr create-repository \
  --repository-name frontend-test \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256
```

**Expected Output:**
```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:928618160741:repository/frontend-test",
        "registryId": "928618160741",
        "repositoryName": "frontend-test",
        "repositoryUri": "928618160741.dkr.ecr.us-east-1.amazonaws.com/frontend-test",
        ...
    }
}
```

## Step 2: Get ECR Repository URL

From the output above, note the `repositoryUri`. It will be in the format:
```
928618160741.dkr.ecr.us-east-1.amazonaws.com/frontend-test
```

Or construct it manually:
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"
REPO_NAME="frontend-test"
ECR_URL="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"
echo $ECR_URL
```

## Step 3: Add to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Add the following secrets:

   **Option A: Just repository name (recommended)**
   - **Name**: `ECR_REPO_NAME`
   - **Value**: `frontend-test`
   
   The workflow will construct the full URL automatically.

   **Option B: Full repository URL**
   - **Name**: `ECR_REPO_URL`
   - **Value**: `928618160741.dkr.ecr.us-east-1.amazonaws.com/frontend-test`
   
   If both are set, `ECR_REPO_URL` takes precedence.

## Step 4: Verify

After adding secrets, the PR workflow will:
1. Read ECR repository name from secret (or use default: `frontend-test`)
2. Verify repository exists in AWS
3. Use it for building and pushing Docker images

## For Production

Create a separate ECR repository for production:

```bash
aws ecr create-repository \
  --repository-name frontend-prod \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256
```

Then add to GitHub secrets:
- `ECR_REPO_NAME_PROD`: `frontend-prod`
- Or `ECR_REPO_URL_PROD`: `928618160741.dkr.ecr.us-east-1.amazonaws.com/frontend-prod`

## Verify Repository Exists

```bash
aws ecr describe-repositories --repository-names frontend-test --region us-east-1
```

## Delete Repository (if needed)

```bash
aws ecr delete-repository \
  --repository-name frontend-test \
  --region us-east-1 \
  --force
```

