# Understanding Cascading Errors in Elastic Beanstalk

## What is a Cascading Error?

When CloudFormation creates resources in a stack, they have **dependencies**:
1. Load Balancer must be created first
2. Target Groups depend on the Load Balancer
3. Auto Scaling Group depends on Target Groups
4. EC2 Instances depend on the Auto Scaling Group

If **any resource fails**, all dependent resources will also fail.

## The Error You're Seeing

```
Resource AWSEBAutoScalingGroup does not exist for stack
```

This is **NOT** an Auto Scaling permission issue. It's a **cascading failure** because:
- The Load Balancer failed to create (due to missing EC2 permissions)
- Because the Load Balancer failed, the Auto Scaling Group can't be created
- CloudFormation reports "Auto Scaling Group does not exist" but the real issue is earlier in the chain

## How to Find the Root Cause

Look for the **FIRST** error in the CloudFormation stack events:

1. Check AWS Console:
   - Go to CloudFormation → Stacks
   - Find the failed stack: `awseb-e-xxxxx-stack`
   - Look at "Events" tab
   - Find the **first** resource that failed (usually `AWSEBV2LoadBalancer`)

2. Check Pulumi output:
   - Look for the **first** error message
   - It will show which resource failed and why
   - Usually something like: "not authorized to perform: ec2:..."

## Current Status

We've been adding EC2 permissions as errors appear:
- ✅ `ec2:CreateSecurityGroup`
- ✅ `ec2:DescribeInternetGateways`
- ✅ `ec2:DescribeAccountAttributes`
- ✅ `iam:CreateServiceLinkedRole`
- ✅ `autoscaling:*` (already had this)

## Next Steps

1. **Update IAM Policy** with all the permissions we've added:
   ```bash
   ./setup-oidc-role.sh
   ```

2. **Clean up the failed environment**:
   ```bash
   ./cleanup-failed-eb-env.sh frontend-test-env frontend-test us-east-1
   ```

3. **Re-run the deployment** - it should now have all required permissions

## If Errors Continue

If you see more permission errors, they will be the **root cause** (the first error in the stack). The Auto Scaling Group error is just a symptom.

Look for errors like:
- `not authorized to perform: ec2:...`
- `not authorized to perform: iam:...`
- `not authorized to perform: elasticloadbalancing:...`

These are the real issues to fix.

