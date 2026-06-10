"""
🇪🇸 Gestión de configuración tipada e inyección de dependencias para infraestructura.
Encapsula acceso centralizado a pulumi.Config y variables de entorno.

🇺🇸 Typed configuration management and dependency injection for infrastructure.
Centralizes access to pulumi.Config and environment variables.
"""

import os
from typing import Dict, Optional
import pulumi

from .constants import DEFAULT_TAGS, DEFAULT_VPN_NAME


class InfrastructureConfig:
    """
    🇪🇸 Configuración centralizada de la infraestructura (Singleton Pattern).
    Proporciona acceso tipado a todas las propiedades de configuración.
    
    🇺🇸 Centralized infrastructure configuration (Singleton Pattern).
    Provides typed access to all configuration properties.
    """

    def __init__(self):
        self._cfg = pulumi.Config()
        self._project_tags = DEFAULT_TAGS

    @property
    def provider(self) -> str:
        """
        🇪🇸 Retorna el proveedor de nube configurado (aws, azure, gcp).
        🇺🇸 Returns the configured cloud provider (aws, azure, gcp).
        """
        provider = self._cfg.get("provider") or os.getenv("PROVIDER")
        return (provider or "aws").lower()

    @property
    def vpn_name(self) -> str:
        """
        🇪🇸 Retorna el nombre base para todos los recursos VPN.
        🇺🇸 Returns the base name for all VPN resources.
        """
        return self._cfg.get("vpn_name") or DEFAULT_VPN_NAME

    @property
    def tags(self) -> Dict[str, str]:
        """
        🇪🇸 Retorna los tags por defecto (aplicados a todos los recursos).
        🇺🇸 Returns default tags (applied to all resources).
        """
        return self._project_tags

    @property
    def aws_region(self) -> str:
        """
        🇪🇸 Retorna la región de AWS configurada.
        🇺🇸 Returns the configured AWS region.
        """
        return self._cfg.get("aws:region") or "us-east-1"

    @property
    def gcp_region(self) -> str:
        """
        🇪🇸 Retorna la región de GCP configurada.
        🇺🇸 Returns the configured GCP region.
        """
        return self._cfg.get("gcp:region") or "us-central1"

    @property
    def azure_location(self) -> str:
        """
        🇪🇸 Retorna la ubicación geográfica de Azure configurada.
        🇺🇸 Returns the configured Azure location (geography).
        """
        return self._cfg.get("azure:location") or "eastus"

    @property
    def vpc_cidr(self) -> str:
        """
        🇪🇸 Retorna el bloque CIDR maestro de la VPC (Network & Subnetting).
        🇺🇸 Returns the master CIDR block for VPC (Network & Subnetting).
        """
        return self._cfg.get("vpc_cidr") or "10.0.0.0/16"

    @property
    def availability_zones(self) -> list[str]:
        """
        🇪🇸 Retorna la lista de zonas de disponibilidad objetivo (High Availability).
        🇺🇸 Returns the target availability zones list (High Availability).
        """
        zones = self._cfg.get_object("availability_zones")
        return zones or ["zone-1", "zone-2"]


# Instancia única de configuración accesible globalmente (Singleton Pattern)
# Single configuration instance accessible globally (Singleton Pattern)
config = InfrastructureConfig()
