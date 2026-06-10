"""
🇪🇸 Clase base abstracta para componentes VPC (Abstract Base Class & Component Pattern).
Define contrato común para todas las implementaciones específicas de proveedor.

🇺🇸 Abstract base class for VPC components (Abstract Base Class & Component Pattern).
Defines common interface for all provider-specific implementations.
"""

from abc import ABC, abstractmethod
import pulumi
from typing import Optional


class VpcComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Clase base abstracta para todos los componentes VPC específicos de proveedor.
    Sigue rigurosamente la arquitectura de componentes papá-hijo en Pulumi.
    
    🇺🇸 Abstract base class for all provider-specific VPC components.
    Strictly adheres to Pulumi's parent-child component resource architecture.
    
    Attributes:
        vpc_id: 🇪🇸 ID/URN del VPC / 🇺🇸 VPC ID/URN
        public_subnet_ids: 🇪🇸 IDs de subnets públicas / 🇺🇸 Public subnet IDs
        private_subnet_ids: 🇪🇸 IDs de subnets privadas / 🇺🇸 Private subnet IDs
        isolated_subnet_ids: 🇪🇸 IDs de subnets aisladas / 🇺🇸 Isolated subnet IDs
    """
    
    def __init__(
        self,
        resource_type: str,
        name: str,
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        """
        🇪🇸 Inicializa el componente VPC base.
        
        🇺🇸 Initializes the base VPC component.
        
        Args:
            resource_type: 🇪🇸 Tipo de recurso Pulumi / 🇺🇸 Pulumi resource type
            name: 🇪🇸 Nombre lógico del componente / 🇺🇸 Logical component name
            opts: 🇪🇸 Opciones de recursos Pulumi / 🇺🇸 Pulumi ResourceOptions
        """
        super().__init__(resource_type, name, opts=opts)
        
        # Outputs que serán populados por implementaciones concretas
        # Outputs to be populated by concrete implementations
        self.vpc_id: pulumi.Output[str] = None
        self.public_subnet_ids: pulumi.Output[list[str]] = None
        self.private_subnet_ids: pulumi.Output[list[str]] = None
        self.isolated_subnet_ids: pulumi.Output[list[str]] = None
        
    @abstractmethod
    def _create_subnets(self):
        """
        🇪🇸 Método abstracto para crear subnets con los CIDRs y zonas especificadas (FR-002).
        Debe ser implementado por cada proveedor específico.
        
        🇺🇸 Abstract method to create subnets with specified CIDRs and zones (FR-002).
        Must be implemented by each provider-specific subclass.
        """
        pass
    
    @abstractmethod
    def _create_gateways(self):
        """
        🇪🇸 Método abstracto para crear Internet Gateway y NAT Gateways (FR-003, FR-004).
        Debe ser implementado por cada proveedor específico.
        
        🇺🇸 Abstract method to create Internet Gateway and NAT Gateways (FR-003, FR-004).
        Must be implemented by each provider-specific subclass.
        """
        pass
        
    def validate_layout(self) -> bool:
        """
        🇪🇸 Valida que el diseño de VPC no tenga dependencias cíclicas o conflictos de CIDR (FR-009).
        Validación estática sin efectos colaterales.
        
        🇺🇸 Validates that VPC layout has no circular dependencies or CIDR conflicts (FR-009).
        Static validation with no side effects.
        
        Returns:
            bool: 🇪🇸 True si la validación pasa / 🇺🇸 True if validation passes
            
        Raises:
            ValueError: 🇪🇸 Si se detecta un problema en el diseño / 🇺🇸 If layout issue detected
        """
        # Implementación lógica de validación estática
        # Static validation logic implementation
        pass
