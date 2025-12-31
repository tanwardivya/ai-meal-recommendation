"""Main Pulumi program - orchestrates all infrastructure components."""
import pulumi
import pulumi_aws as aws
from infrastructure.components.ecr import ECRComponent
from infrastructure.components.elasticbeanstalk import ElasticBeanstalkComponent
from infrastructure.config import get_config


# Load configuration
config = get_config()
stack = pulumi.get_stack()
env = config["environment"]

# Create ECR repository for frontend Docker images
ecr = ECRComponent(
    f"{stack}-ecr",
    config["ecr"]
)

# Create IAM service role for Elastic Beanstalk
# This role allows EB to manage AWS resources on your behalf
eb_service_role = aws.iam.Role(
    f"{stack}-eb-service-role",
    assume_role_policy=pulumi.Output.from_input({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "elasticbeanstalk.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "elasticbeanstalk"
                }
            }
        }]
    }),
    tags=config["tags"],
    opts=pulumi.ResourceOptions()
)

# Attach AWS managed policy for Elastic Beanstalk service role
aws.iam.RolePolicyAttachment(
    f"{stack}-eb-service-role-policy",
    role=eb_service_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService",
    opts=pulumi.ResourceOptions(parent=eb_service_role)
)

# Attach additional policies for enhanced health reporting
aws.iam.RolePolicyAttachment(
    f"{stack}-eb-enhanced-health-policy",
    role=eb_service_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth",
    opts=pulumi.ResourceOptions(parent=eb_service_role)
)

# Create IAM instance profile for EC2 instances in Elastic Beanstalk
# This allows EC2 instances to access AWS services
eb_instance_profile_role = aws.iam.Role(
    f"{stack}-eb-instance-profile-role",
    assume_role_policy=pulumi.Output.from_input({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }),
    tags=config["tags"],
    opts=pulumi.ResourceOptions()
)

# Attach AWS managed policy for EC2 instances
aws.iam.RolePolicyAttachment(
    f"{stack}-eb-instance-profile-policy",
    role=eb_instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier",
    opts=pulumi.ResourceOptions(parent=eb_instance_profile_role)
)

aws.iam.RolePolicyAttachment(
    f"{stack}-eb-instance-profile-worker-policy",
    role=eb_instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWorkerTier",
    opts=pulumi.ResourceOptions(parent=eb_instance_profile_role)
)

# Attach ECR read policy so instances can pull images
ecr_read_policy = aws.iam.Policy(
    f"{stack}-eb-ecr-read-policy",
    description="Allow EC2 instances to pull images from ECR",
    policy=pulumi.Output.all(ecr.repository_arn).apply(
        lambda args: {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage"
                ],
                "Resource": "*"
            }, {
                "Effect": "Allow",
                "Action": [
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage"
                ],
                "Resource": args[0]
            }]
        }
    ),
    tags=config["tags"],
    opts=pulumi.ResourceOptions(parent=eb_instance_profile_role)
)

aws.iam.RolePolicyAttachment(
    f"{stack}-eb-ecr-read-policy-attachment",
    role=eb_instance_profile_role.name,
    policy_arn=ecr_read_policy.arn,
    opts=pulumi.ResourceOptions(parent=eb_instance_profile_role)
)

# Create instance profile
eb_instance_profile = aws.iam.InstanceProfile(
    f"{stack}-eb-instance-profile",
    role=eb_instance_profile_role.name,
    tags=config["tags"],
    opts=pulumi.ResourceOptions(parent=eb_instance_profile_role)
)

# Create Elastic Beanstalk application and environment
elasticbeanstalk = ElasticBeanstalkComponent(
    f"{stack}-eb",
    config["elasticbeanstalk"],
    service_role_arn=eb_service_role.arn,
    instance_profile_arn=eb_instance_profile.arn,
)

# Export outputs
pulumi.export("ecr_repository_url", ecr.url)
pulumi.export("ecr_repository_name", ecr.repository_name)
pulumi.export("ecr_repository_arn", ecr.repository_arn)
pulumi.export("eb_application_name", elasticbeanstalk.application_name)
pulumi.export("eb_environment_name", elasticbeanstalk.environment_name)
pulumi.export("eb_environment_url", elasticbeanstalk.environment_url)
pulumi.export("eb_environment_id", elasticbeanstalk.environment_id)

