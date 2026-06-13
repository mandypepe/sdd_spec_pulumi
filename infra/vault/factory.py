import pulumi
from typing import Dict, Type
from infra.vault.base import VaultComponentResource

class VaultProviderFactory:
    """
    🇪🇸 Fábrica para instanciar componentes de Bóveda de Secretos basados en el proveedor.
    🇺🇸 Factory to instantiate Secrets Vault components based on provider.
    """
    _providers: Dict[str, Type[VaultComponentResource]] = {}

    @classmethod
    def register(cls, provider: str, component_class: Type[VaultComponentResource]):
        cls._providers[provider.lower()] = component_class

    @classmethod
    def get_component(cls, provider: str, name: str, opts: pulumi.ResourceOptions = None) -> VaultComponentResource:
        component_class = cls._providers.get(provider.lower())
        if not component_class:
            raise ValueError(f"Vault provider '{provider}' not registered.")
        return component_class(name, opts=opts)
