"""Base component class for Pulumi components."""
import pulumi


class BaseComponent(pulumi.ComponentResource):
    """Base class for all Pulumi components."""
    
    def __init__(self, name: str, component_type: str, opts=None):
        super().__init__(component_type, name, {}, opts)
        self.name = name


