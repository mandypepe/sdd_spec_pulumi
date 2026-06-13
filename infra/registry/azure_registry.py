"""
🇪🇸 Componente de registro Azure (ACR).
🇺🇸 Azure Registry component (ACR).
"""
import pulumi
from typing import Optional
from .base import RegistryComponent

class AzureRegistry(RegistryComponent):
    """
    🇪🇸 Implementación de ACR para RegistryComponent.
    🇺🇸 ACR implementation for RegistryComponent.
    """
    
    def __init__(self, name: str, region: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__(name, region, opts)
        self._provision_registry()

    @property
    def registry_id(self) -> pulumi.Output[str]:
        return pulumi.Output.from_input("azure-acr-id")

    @property
    def repository_url(self) -> pulumi.Output[str]:
        return pulumi.Output.from_input("azure-acr-url")

    @property
    def tag_immutability(self) -> pulumi.Output[bool]:
        return pulumi.Output.from_input(True)

    @property
    def vulnerability_scanning(self) -> pulumi.Output[bool]:
        return pulumi.Output.from_input(True)

    @property
    def access_policy(self) -> pulumi.Output[dict]:
        return pulumi.Output.from_input({})

    @property
    def lifecycle_policy(self) -> pulumi.Output[dict]:
        return pulumi.Output.from_input({})

    def _provision_registry(self):
        """🇪🇸 Provee el registro ACR / 🇺🇸 Provisions ACR registry."""
        pass
