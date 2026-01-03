# Cleaning Up Failed Elastic Beanstalk Environment

When an Elastic Beanstalk environment fails to create (e.g., due to missing IAM permissions), it enters a `CREATE_FAILED` state. You need to clean it up before Pulumi can recreate it.

## Option 1: Use the Cleanup Script (Recommended)

```bash
# Clean up the test environment
./cleanup-failed-eb-env.sh frontend-test-env frontend-test us-east-1

# Or for production
./cleanup-failed-eb-env.sh frontend-prod-env frontend-prod us-east-1
```

## Option 2: Manual AWS CLI Commands

```bash
# Terminate the failed environment
aws elasticbeanstalk terminate-environment \
  --environment-name frontend-test-env \
  --region us-east-1 \
  --force-terminate

# Wait for termination (check status)
aws elasticbeanstalk describe-environments \
  --environment-names frontend-test-env \
  --region us-east-1 \
  --query 'Environments[0].Status' \
  --output text
```

## Option 3: Using Pulumi Destroy

If you prefer to use Pulumi:

```bash
cd infrastructure
source .venv/bin/activate
pulumi stack select test
pulumi destroy --yes
```

Then re-run the deployment workflow.

## Option 4: AWS Console

1. Go to AWS Elastic Beanstalk Console
2. Select the application (`frontend-test`)
3. Find the failed environment (`frontend-test-env`)
4. Click "Actions" → "Terminate Environment"
5. Confirm termination

## After Cleanup

Once the environment is terminated:

1. **Update IAM Policy** (if you haven't already):
   ```bash
   ./setup-oidc-role.sh
   ```

2. **Re-run the deployment workflow** - Pulumi will create a fresh environment with the correct permissions.

## Why This Happens

When Elastic Beanstalk fails to create resources (due to missing permissions, invalid configuration, etc.), the underlying CloudFormation stack enters a `CREATE_FAILED` state. AWS doesn't allow updating or recreating environments in this state - you must terminate them first.

