import pulumi
from abc import ABC, abstractmethod
from typing import Dict, Type

class OrchestratorComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Componente base abstracto para orquestadores Kubernetes.
    🇺🇸 Abstract base component for Kubernetes orchestrators.
    """
    def __init__(self, resource_type: str, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__(resource_type, name, opts=opts)

    @abstractmethod
    def provision(self):
        """Provision orchestrator and node pools"""
        pass

    @abstractmethod
    def configure_security(self):
        """Configure perimeter security"""
        pass

    @abstractmethod
    def configure_identity(self):
        """Configure federated identity"""
        pass

class OrchestratorProviderFactory:
    """
    🇪🇸 Fábrica para instanciar componentes de orquestador basados en el proveedor.
    🇺🇸 Factory to instantiate orchestrator components based on provider.
    """
    _providers: Dict[str, Type[OrchestratorComponent]] = {}

    @classmethod
    def register(cls, provider: str, component_class: Type[OrchestratorComponent]):
        cls._providers[provider.lower()] = component_class

    @classmethod
    def get_component(cls, provider: str, name: str, opts: pulumi.ResourceOptions = None) -> OrchestratorComponent:
        component_class = cls._providers.get(provider.lower())
        if not component_class:
            raise ValueError(f"Provider '{provider}' not registered.")
        return component_class(name, opts=opts)
