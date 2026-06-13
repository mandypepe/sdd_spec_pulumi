import pulumi
from typing import Dict, Type
from infra.identity.base import BaseIdentityComponent
from infra.identity.aws_identity import AwsIdentityComponent
from infra.identity.azure_identity import AzureIdentityComponent
from infra.identity.gcp_identity import GcpIdentityComponent

class IdentityProviderFactory:
    """
    Factory for creating Identity Provider components.
    (Spanish) Fábrica para crear componentes de Proveedor de Identidad.
    """

    _providers: Dict[str, Type[BaseIdentityComponent]] = {
        "aws": AwsIdentityComponent,
        "azure": AzureIdentityComponent,
        "gcp": GcpIdentityComponent,
    }

    @classmethod
    def create(cls, provider: str, resource_name: str, opts: pulumi.ResourceOptions = None) -> BaseIdentityComponent:
        """
        Creates an Identity Provider component based on the provider name.
        (Spanish) Crea un componente de Proveedor de Identidad basado en el nombre del proveedor.
        """
        provider_class = cls._providers.get(provider.lower())
        if not provider_class:
            raise ValueError(f"Unknown identity provider: {provider}")
        return provider_class(resource_name, opts)
