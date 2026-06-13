"""
🇪🇸 Factory para seleccionar los proveedores de seguridad (Factory Pattern).
🇺🇸 Factory for selecting security providers (Factory Pattern).
"""

from typing import Dict, Optional, Type
import pulumi
from .base import SecurityComponent
from .aws_security import AwsSecurity
from .azure_security import AzureSecurity
from .gcp_security import GcpSecurity

class SecurityProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes de Seguridad.
    🇺🇸 Factory for Security component creation.
    """

    _PROVIDERS: Dict[str, Type[SecurityComponent]] = {
        "aws": AwsSecurity,
        "azure": AzureSecurity,
        "gcp": GcpSecurity,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, tier: str, opts: Optional[pulumi.ResourceOptions] = None) -> SecurityComponent:
        provider = (provider_name or "").lower()
        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(f"Unsupported provider: '{provider_name}'. Supported: {supported}")
        
        security_class = cls._PROVIDERS[provider]
        return security_class(f"custom:{provider}:SecurityPerimeter", name, tier, opts=opts)
