"""Elastic Beanstalk component - application deployment platform."""
import pulumi
import pulumi_aws as aws
from infrastructure.components.base import BaseComponent
from infrastructure.config_types.elasticbeanstalk_config import ElasticBeanstalkConfig


class ElasticBeanstalkComponent(BaseComponent):
    """Reusable Elastic Beanstalk component."""
    
    def __init__(
        self,
        name: str,
        config: ElasticBeanstalkConfig,
        service_role_arn: str = None,
        instance_profile_arn: str = None,
        opts=None
    ):
        super().__init__(name, "custom:components:ElasticBeanstalk", opts)
        
        # Create Elastic Beanstalk application
        self.application = aws.elasticbeanstalk.Application(
            f"{name}-app",
            name=config.application_name,
            description=f"Elastic Beanstalk application for {name}",
            appversion_lifecycle=aws.elasticbeanstalk.ApplicationAppversionLifecycleArgs(
                max_count=10,
                delete_source_from_s3=True,
            ),
            tags=config.tags or {},
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Build setting list for environment
        settings = []
        
        # Solution stack name
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:platform",
            name="Platform",
            value=config.solution_stack_name,
        ))
        
        # Instance type
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:launchconfiguration",
            name="InstanceType",
            value=config.instance_type,
        ))
        
        # Auto Scaling settings
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:asg",
            name="MinSize",
            value=str(config.min_size),
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:asg",
            name="MaxSize",
            value=str(config.max_size),
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:trigger",
            name="MeasureName",
            value="CPUUtilization",
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:trigger",
            name="Statistic",
            value="Average",
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:trigger",
            name="Unit",
            value="Percent",
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:trigger",
            name="UpperThreshold",
            value="80",
        ))
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:trigger",
            name="LowerThreshold",
            value="20",
        ))
        
        # Health reporting
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:healthreporting:system",
            name="SystemType",
            value="enhanced",
        ))
        
        # Load balancer type (Application Load Balancer)
        settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:environment",
            name="LoadBalancerType",
            value="application",
        ))
        
        # Environment variables
        if config.environment_variables:
            for key, value in config.environment_variables.items():
                settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name=key,
                    value=value,
                ))
        
        # VPC configuration if provided
        if config.vpc_id and config.subnet_ids:
            settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                namespace="aws:ec2:vpc",
                name="VPCId",
                value=config.vpc_id,
            ))
            settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                namespace="aws:ec2:vpc",
                name="Subnets",
                value=",".join(config.subnet_ids),
            ))
            if config.public_subnet_ids:
                settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="ELBSubnets",
                    value=",".join(config.public_subnet_ids),
                ))
            settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                namespace="aws:ec2:vpc",
                name="AssociatePublicIpAddress",
                value="false",
            ))
        
        # Service role (required for EB)
        if service_role_arn:
            settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                namespace="aws:elasticbeanstalk:environment",
                name="ServiceRole",
                value=service_role_arn,
            ))
        
        # Instance profile (for EC2 instances)
        if instance_profile_arn:
            settings.append(aws.elasticbeanstalk.EnvironmentSettingArgs(
                namespace="aws:autoscaling:launchconfiguration",
                name="IamInstanceProfile",
                value=instance_profile_arn,
            ))
        
        # Create Elastic Beanstalk environment
        self.environment = aws.elasticbeanstalk.Environment(
            f"{name}-env",
            name=config.environment_name,
            application=self.application.name,
            solution_stack_name=config.solution_stack_name,
            settings=settings,
            tags=config.tags or {},
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=[self.application]
            )
        )
        
        # Register outputs
        self.register_outputs({
            "application_name": self.application.name,
            "environment_name": self.environment.name,
            "environment_url": self.environment.endpoint_url,
            "environment_id": self.environment.id,
            "environment_arn": self.environment.arn,
        })
    
    @property
    def application_name(self):
        return self.application.name
    
    @property
    def environment_name(self):
        return self.environment.name
    
    @property
    def environment_url(self):
        return self.environment.endpoint_url
    
    @property
    def environment_id(self):
        return self.environment.id
    
    @property
    def environment_arn(self):
        return self.environment.arn

