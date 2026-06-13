"""
🇪🇸 Componente base abstracto para seguridad perimetral (Abstract Base Class & Component Pattern).
Define contrato para firewalls perimetrales multi-proveedor.

🇺🇸 Abstract base class for perimeter security (Abstract Base Class & Component Pattern).
Defines contract for multi-provider perimeter firewalls.
"""

from abc import ABC, abstractmethod
import pulumi
from typing import Optional


class SecurityComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Componente base para firewalls perimetrales (Public, Compute, Data).
    🇺🇸 Base component for perimeter firewalls (Public, Compute, Data).
    """
    
    def __init__(
        self,
        resource_type: str,
        name: str,
        tier: str,
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        super().__init__(resource_type, name, opts=opts)
        self.tier = tier
        self.resource_id: pulumi.Output[str] = None
        
    @abstractmethod
    def _create_firewall_rules(self):
        """🇪🇸 Implementar reglas de firewall específicas del proveedor. / 🇺🇸 Implement provider-specific firewall rules."""
        pass
    
    @abstractmethod
    def _configure_logging(self):
        """🇪🇸 Configurar logging y retención (FR-009). / 🇺🇸 Configure logging and retention (FR-009)."""
        pass
