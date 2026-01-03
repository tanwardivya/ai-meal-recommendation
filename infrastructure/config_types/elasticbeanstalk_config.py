"""Elastic Beanstalk configuration types."""
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class ElasticBeanstalkConfig:
    """Configuration for Elastic Beanstalk component."""
    application_name: str
    environment_name: str
    solution_stack_name: str = "Docker running on 64bit Amazon Linux 2"
    instance_type: str = "t3.small"
    min_size: int = 1
    max_size: int = 4
    desired_capacity: int = 1
    environment_variables: Optional[Dict[str, str]] = None
    vpc_id: Optional[str] = None
    subnet_ids: Optional[List[str]] = None
    public_subnet_ids: Optional[List[str]] = None
    tags: Optional[dict] = None


