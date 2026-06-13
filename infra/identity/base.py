import pulumi
from abc import ABC, abstractmethod

class BaseIdentityComponent(pulumi.ComponentResource, ABC):
    """
    Abstract base class for all Identity Provider components.
    遵循 (Spanish) Sigue el principio de responsabilidad única (SRP).
    (English) Follows the Single Responsibility Principle (SRP).
    """

    def __init__(self, resource_name: str, opts: pulumi.ResourceOptions = None):
        # Ensure deletion protection is enabled by default for identity resources
        protection_opts = pulumi.ResourceOptions(protect=True).merge(opts)
        super().__init__("custom:identity:BaseIdentityComponent", resource_name, {}, protection_opts)

    @abstractmethod
    def get_token_endpoint(self) -> str:
        """
        Returns the OIDC token endpoint for the provider.
        (Spanish) Retorna el endpoint del token OIDC para el proveedor.
        """
        pass

    @abstractmethod
    def apply_boundary_policy(self, policy_arn: str):
        """
        Applies a boundary policy to the federated identity.
        (Spanish) Aplica una política de límites a la identidad federada.
        """
        pass
