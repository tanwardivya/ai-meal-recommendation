"""ECR configuration types."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ECRConfig:
    """Configuration for ECR component."""
    repository_name: str
    image_tag_mutability: str = "MUTABLE"  # MUTABLE or IMMUTABLE
    image_scanning_enabled: bool = True
    encryption_type: str = "AES256"  # AES256 or KMS
    lifecycle_policy_enabled: bool = True
    max_image_count: int = 10  # Keep last N images
    tags: Optional[dict] = None

