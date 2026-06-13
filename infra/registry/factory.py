"""
🇪🇸 Factory para la creación de componentes de Registro (RegistryComponent).
🇺🇸 Factory for Registry component creation.
"""
import pulumi
from typing import Dict, Optional, Type
from .base import RegistryComponent
# Import concrete registries later
# from .aws_registry import AwsRegistry
# from .azure_registry import AzureRegistry
# from .gcp_registry import GcpRegistry

class RegistryProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes de Registro.
    🇺🇸 Factory for Registry component creation.
    """
    
    _PROVIDERS: Dict[str, Type[RegistryComponent]] = {
        # "aws": AwsRegistry,
        # "azure": AzureRegistry,
        # "gcp": GcpRegistry,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, region: str, opts: Optional[pulumi.ResourceOptions] = None) -> RegistryComponent:
        provider = (provider_name or "").lower()
        if provider not in cls._PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")
        return cls._PROVIDERS[provider](name=name, region=region, opts=opts)
