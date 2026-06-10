from abc import ABC, abstractmethod
import pulumi
from typing import Optional

class VpcComponent(pulumi.ComponentResource, ABC):
    """
    Abstract base class for all provider-specific VPC implementations.
    Strictly follows the component-based architecture by parenting child resources.
    """
    def __init__(self, resource_type: str, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__(resource_type, name, opts=opts)
        self.vpc_id: pulumi.Output[str] = None # To be populated by concrete implementations
        self.public_subnet_ids: pulumi.Output[list[str]] = None
        self.private_subnet_ids: pulumi.Output[list[str]] = None
        self.isolated_subnet_ids: pulumi.Output[list[str]] = None
        
    @abstractmethod
    def _create_subnets(self):
        pass
    
    @abstractmethod
    def _create_gateways(self):
        pass
        
    def validate_layout(self):
        """
        🇪🇸 Valida que el diseño no tenga dependencias cíclicas.
        🇺🇸 Validate that the layout has no circular dependencies.
        """
        # (Implementación lógica de validación estática)
        pass
