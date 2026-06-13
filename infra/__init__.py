"""Paquete infra: componentes reutilizables para el proyecto Pulumi multi-cloud.

Este paquete expone fábricas y componentes de alto nivel y mantiene la
separación entre la API del usuario y las implementaciones proveedor-específicas.
"""

from .providers import VpnProviderFactory, VpcProviderFactory, LbProviderFactory, SupportedProviders
from .vault.factory import VaultProviderFactory

__all__ = [
    "VpnProviderFactory", 
    "VpcProviderFactory", 
    "LbProviderFactory", 
    "VaultProviderFactory",
    "SupportedProviders"
]
