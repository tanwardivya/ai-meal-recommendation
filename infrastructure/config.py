"""Configuration management for Pulumi stacks."""
import pulumi
from infrastructure.config_types.ecr_config import ECRConfig
from infrastructure.config_types.elasticbeanstalk_config import ElasticBeanstalkConfig


def get_config():
    """Load and return configuration for current stack."""
    config = pulumi.Config()
    stack = pulumi.get_stack()
    
    # Get environment
    environment = config.get("environment") or stack
    
    # Base tags
    base_tags = {
        "Environment": environment,
        "ManagedBy": "Pulumi",
        "Project": config.get("projectName") or "ai-meal-recommendation",
    }
    
    # ECR config
    ecr_repository_name = config.get("ecrRepositoryName") or f"frontend-{environment}"
    ecr_config = ECRConfig(
        repository_name=ecr_repository_name,
        image_scanning_enabled=config.get_bool("ecrImageScanning") if config.get("ecrImageScanning") else True,
        lifecycle_policy_enabled=config.get_bool("ecrLifecyclePolicy") if config.get("ecrLifecyclePolicy") else True,
        max_image_count=config.get_int("ecrMaxImageCount") or 10,
        tags=base_tags,
    )
    
    # Elastic Beanstalk config
    eb_application_name = config.get("ebApplicationName") or f"frontend-{environment}"
    eb_environment_name = config.get("ebEnvironmentName") or f"frontend-{environment}-env"
    
    # Parse environment variables from config
    env_vars = {}
    env_vars_config = config.get_object("ebEnvironmentVariables") or {}
    if isinstance(env_vars_config, dict):
        env_vars = env_vars_config
    
    eb_config = ElasticBeanstalkConfig(
        application_name=eb_application_name,
        environment_name=eb_environment_name,
        solution_stack_name=config.get("ebSolutionStack") or "Docker running on 64bit Amazon Linux 2",
        instance_type=config.get("ebInstanceType") or "t3.small",
        min_size=config.get_int("ebMinSize") or 1,
        max_size=config.get_int("ebMaxSize") or 4,
        desired_capacity=config.get_int("ebDesiredCapacity") or 1,
        environment_variables=env_vars if env_vars else None,
        vpc_id=config.get("vpcId"),
        subnet_ids=config.get_object("subnetIds") if config.get("subnetIds") else None,
        public_subnet_ids=config.get_object("publicSubnetIds") if config.get("publicSubnetIds") else None,
        tags=base_tags,
    )
    
    return {
        "environment": environment,
        "ecr": ecr_config,
        "elasticbeanstalk": eb_config,
        "tags": base_tags,
    }


