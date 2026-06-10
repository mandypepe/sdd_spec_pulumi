"""
🇪🇸 Definición base de un componente VPN reutilizable.
Garantiza que las implementaciones de proveedores respeten la misma API.

🇺🇸 Base definition for a reusable VPN component.
Ensures provider implementations adhere to the same API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import pulumi


class VpnComponent(pulumi.ComponentResource, ABC):
    """Interfaz base para componentes VPN.

    Aplica el principio de Abstracción para garantizar que todas las
    implementaciones de proveedores expongan una interfaz consistente.
    """

    def __init__(self, resource_type: str, name: str, opts: pulumi.ResourceOptions | None = None):
        """Inicializa el componente VPN.

        Args:
            resource_type: El tipo de recurso de Pulumi (ej: 'infra:aws:Vpn').
            name: El nombre lógico del recurso.
            opts: Opciones adicionales de Pulumi.
        """
        super().__init__(resource_type, name, None, opts)
        self.resource_name = name

    @abstractmethod
    def get_outputs(self) -> Dict[str, Any]:
        """Devuelve un diccionario con las salidas del componente.

        Este método debe ser implementado por cada proveedor para mapear
        sus recursos específicos a un formato común si es posible.
        """
        raise NotImplementedError()

