"""
🇪🇸 Componente base para Container Registry (RegistryComponent).
🇺🇸 Base component for Container Registry (RegistryComponent).
"""
import pulumi
from abc import ABC, abstractmethod
from typing import Optional

class RegistryComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Componente base para definir registros de contenedores multi-cloud.
    🇺🇸 Base component to define multi-cloud container registries.
    """
    
    def __init__(self, name: str, region: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("custom:infra:RegistryComponent", name, {}, opts)
        self.name = name
        self.region = region

    @property
    @abstractmethod
    def registry_id(self) -> pulumi.Output[str]:
        """🇪🇸 Devuelve el ID del registro / 🇺🇸 Returns registry ID."""
        pass

    @property
    @abstractmethod
    def repository_url(self) -> pulumi.Output[str]:
        """🇪🇸 Devuelve la URL del repositorio / 🇺🇸 Returns repository URL."""
        pass

    @property
    @abstractmethod
    def tag_immutability(self) -> pulumi.Output[bool]:
        """🇪🇸 Retorna estado de inmutabilidad / 🇺🇸 Returns immutability status."""
        pass

    @property
    @abstractmethod
    def vulnerability_scanning(self) -> pulumi.Output[bool]:
        """🇪🇸 Retorna estado de escaneo / 🇺🇸 Returns scanning status."""
        pass

    @property
    @abstractmethod
    def access_policy(self) -> pulumi.Output[dict]:
        """🇪🇸 Retorna política de acceso / 🇺🇸 Returns access policy."""
        pass

    @property
    @abstractmethod
    def lifecycle_policy(self) -> pulumi.Output[dict]:
        """🇪🇸 Retorna política de ciclo de vida / 🇺🇸 Returns lifecycle policy."""
        pass

    @abstractmethod
    def _provision_registry(self):
        """🇪🇸 Provee el registro base / 🇺🇸 Provisions the base registry."""
        pass
