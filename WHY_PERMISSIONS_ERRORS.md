# Why Are We Getting Permission Errors?

## Root Cause

When Elastic Beanstalk creates an environment, it uses **CloudFormation** to create multiple AWS resources:
1. **Load Balancer** (Application Load Balancer)
2. **EC2 Instances** (Auto Scaling Group)
3. **Security Groups**
4. **Target Groups**
5. **Service-Linked Roles**

During this process, AWS services need to:
- Check account attributes (quotas, limits)
- Describe VPC resources
- Create networking resources
- Verify permissions

## The Problem

The **GitHub Actions IAM role** (`github-actions-frontend-role`) needs permissions for:
1. **Pulumi** to create/manage resources
2. **Elastic Beanstalk** to create environments
3. **CloudFormation** (used by EB) to create resources
4. **EC2** operations (for load balancers, security groups, etc.)
5. **IAM** operations (for service-linked roles)

## Why Errors Keep Appearing

AWS services call other services during resource creation:
- **Elastic Load Balancing** → calls **EC2** to check account attributes
- **CloudFormation** → calls multiple services to create resources
- Each service needs specific permissions

We've been adding permissions **reactively** (as errors occur), but AWS has many service-to-service calls that require specific permissions.

## Solution

I've added `ec2:DescribeAccountAttributes` to the policy. This permission allows Elastic Load Balancing to check account attributes when creating a load balancer.

## Next Steps

1. **Update the IAM policy** (run `./setup-oidc-role.sh`)
2. **Re-run the deployment**
3. If more errors appear, we'll add those permissions too

## Alternative: Broader Permissions

If errors continue, we could grant broader EC2 permissions:
- `ec2:Describe*` - All describe operations
- `ec2:*` - All EC2 operations (less secure, but comprehensive)

However, the current approach (adding specific permissions) is more secure and follows the principle of least privilege.

