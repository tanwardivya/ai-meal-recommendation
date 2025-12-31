"""ECR component - Docker image repository."""
import json
import pulumi
import pulumi_aws as aws
from infrastructure.components.base import BaseComponent
from infrastructure.config_types.ecr_config import ECRConfig


class ECRComponent(BaseComponent):
    """Reusable ECR component for Docker image storage."""
    
    def __init__(self, name: str, config: ECRConfig, opts=None):
        super().__init__(name, "custom:components:ECR", opts)
        
        # Create ECR repository
        # force_delete=True allows deletion even when repository contains images
        self.repository = aws.ecr.Repository(
            f"{name}-repo",
            name=config.repository_name,
            image_tag_mutability=config.image_tag_mutability,
            image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
                scan_on_push=config.image_scanning_enabled
            ),
            encryption_configurations=[aws.ecr.RepositoryEncryptionConfigurationArgs(
                encryption_type=config.encryption_type
            )],
            force_delete=True,  # Allow deletion even when repository contains images
            tags=config.tags or {},
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Create lifecycle policy to keep only last N images
        if config.lifecycle_policy_enabled:
            lifecycle_policy = {
                "rules": [
                    {
                        "rulePriority": 1,
                        "description": "Keep last N images",
                        "selection": {
                            "tagStatus": "any",
                            "countType": "imageCountMoreThan",
                            "countNumber": config.max_image_count
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }
            
            self.lifecycle_policy = aws.ecr.LifecyclePolicy(
                f"{name}-lifecycle",
                repository=self.repository.name,
                policy=json.dumps(lifecycle_policy),
                opts=pulumi.ResourceOptions(parent=self)
            )
        
        # Get repository URL (region will be resolved at runtime)
        aws_config = pulumi.Config("aws")
        aws_region = aws_config.get("region") or "us-east-1"
        
        self.repository_url = pulumi.Output.all(
            self.repository.registry_id,
            self.repository.name
        ).apply(lambda args: f"{args[0]}.dkr.ecr.{aws_region}.amazonaws.com/{args[1]}")
        
        # Register outputs
        self.register_outputs({
            "repository_url": self.repository_url,
            "repository_arn": self.repository.arn,
            "repository_name": self.repository.name,
            "registry_id": self.repository.registry_id,
        })
    
    @property
    def url(self):
        return self.repository_url
    
    @property
    def repository_name(self):
        return self.repository.name
    
    @property
    def repository_arn(self):
        return self.repository.arn

