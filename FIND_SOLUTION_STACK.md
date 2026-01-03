# Finding the Correct Elastic Beanstalk Solution Stack

The solution stack name must match exactly what's available in your AWS region. Run this command to find the correct name:

```bash
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`) && contains(@, `Amazon Linux 2`)]' \
  --output table
```

Or to get just the most recent one:

```bash
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`) && contains(@, `Amazon Linux 2`)] | [0]' \
  --output text
```

## Common Solution Stack Names

Based on AWS documentation, common Docker solution stacks include:
- `64bit Amazon Linux 2 v3.8.0 running Docker`
- `64bit Amazon Linux 2 v3.7.0 running Docker`
- `64bit Amazon Linux 2 v3.6.0 running Docker`
- `64bit Amazon Linux 2 v3.5.0 running Docker`

## Update Configuration

Once you find the correct solution stack name, update it in:

1. **Pulumi.test.yaml**:
   ```yaml
   frontend-infrastructure:ebSolutionStack: "64bit Amazon Linux 2 v3.X.X running Docker"
   ```

2. **Pulumi.prod.yaml**:
   ```yaml
   frontend-infrastructure:ebSolutionStack: "64bit Amazon Linux 2 v3.X.X running Docker"
   ```

Replace `v3.X.X` with the actual version number from the AWS CLI output.

## Alternative: Use Platform Branch

If the exact version doesn't work, you can try using a platform branch (currently set to):
- `Docker running on 64bit Amazon Linux 2`

This is more stable but may not be supported in all regions.

