"""
🇪🇸 Clase base abstracta para componentes de Load Balancer (Abstract Base Class & Component Pattern).
Define el contrato común para todas las implementaciones de proveedores de LB.

🇺🇸 Abstract base class for Load Balancer components (Abstract Base Class & Component Pattern).
Defines the common contract for all LB provider implementations.
"""

from abc import ABC, abstractmethod
import pulumi
from typing import Optional, List


class LbComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Clase base abstracta para todos los componentes de Load Balancer específicos de proveedor.
    Sigue la arquitectura de componentes de Pulumi.
    
    🇺🇸 Abstract base class for all provider-specific Load Balancer components.
    Follows Pulumi's component resource architecture.
    """
    
    def __init__(
        self,
        resource_type: str,
        name: str,
        vpc_id: pulumi.Input[str],
        public_subnet_ids: pulumi.Input[List[str]],
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        """
        🇪🇸 Inicializa el componente de Load Balancer base.
        
        🇺🇸 Initializes the base Load Balancer component.
        
        Args:
            resource_type: 🇪🇸 Tipo de recurso Pulumi / 🇺🇸 Pulumi resource type
            name: 🇪🇸 Nombre lógico del componente / 🇺🇸 Logical component name
            vpc_id: 🇪🇸 ID del VPC / 🇺🇸 VPC ID
            public_subnet_ids: 🇪🇸 IDs de las subnets públicas / 🇺🇸 Public subnet IDs
            opts: 🇪🇸 Opciones de recursos Pulumi / 🇺🇸 Pulumi ResourceOptions
        """
        super().__init__(resource_type, name, None, opts)
        self.vpc_id = vpc_id
        self.public_subnet_ids = public_subnet_ids
        
        # Outputs que serán populados por implementaciones concretas
        # Outputs to be populated by concrete implementations
        self.dns_name: pulumi.Output[str] = None
        self.lb_arn_or_id: pulumi.Output[str] = None
        self.security_group_id: pulumi.Output[str] = None

    @abstractmethod
    def _create_load_balancer(self):
        """
        🇪🇸 Método abstracto para crear el recurso de Load Balancer.
        
        🇺🇸 Abstract method to create the Load Balancer resource.
        """
        pass

    @abstractmethod
    def _create_listener(self, certificate_arn_or_id: str):
        """
        🇪🇸 Método abstracto para crear el listener HTTPS.
        
        🇺🇸 Abstract method to create the HTTPS listener.
        """
        pass

    @abstractmethod
    def _create_target_group(self):
        """
        🇪🇸 Método abstracto para crear el grupo de destino (Target Group).
        
        🇺🇸 Abstract method to create the target group.
        """
        pass
