"""
🇪🇸 Gestión de configuración tipada para la infraestructura.
Encapsula el acceso a pulumi.Config y variables de entorno.

🇺🇸 Typed configuration management for infrastructure.
Encapsulates access to pulumi.Config and environment variables.
"""

import os
from typing import Dict, Optional
import pulumi

from .constants import DEFAULT_TAGS, DEFAULT_VPN_NAME


class InfrastructureConfig:
    """Configuración centralizada de la infraestructura."""

    def __init__(self):
        self._cfg = pulumi.Config()
        self._project_tags = DEFAULT_TAGS

    @property
    def provider(self) -> str:
        """Retorna el proveedor de nube (aws, azure, gcp)."""
        provider = self._cfg.get("provider") or os.getenv("PROVIDER")
        return (provider or "aws").lower()

    @property
    def vpn_name(self) -> str:
        """Retorna el nombre base para los recursos VPN."""
        return self._cfg.get("vpn_name") or DEFAULT_VPN_NAME

    @property
    def tags(self) -> Dict[str, str]:
        """Retorna los tags por defecto para todos los recursos."""
        return self._project_tags

    @property
    def aws_region(self) -> str:
        """Retorna la región de AWS."""
        return self._cfg.get("aws:region") or "us-east-1"

    @property
    def gcp_region(self) -> str:
        """Retorna la región de GCP."""
        return self._cfg.get("gcp:region") or "us-central1"

    @property
    def azure_location(self) -> str:
        """Retorna la ubicación de Azure."""
        return self._cfg.get("azure:location") or "eastus"


# Instancia única de configuración (Pattern: Singleton-like access)
config = InfrastructureConfig()
