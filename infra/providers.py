"""
🇪🇸 Fábrica para seleccionar el proveedor VPN (Patrón Factory & OCP).
Permite la extensión de proveedores sin modificar la lógica central.

🇺🇸 Factory for selecting the VPN provider (Factory Pattern & OCP).
Allows provider extension without modifying core logic.
"""

from typing import Dict, Optional, Type
import pulumi

from .vpn.base import VpnComponent
from .vpn.aws_vpn import AwsVpn
from .vpn.azure_vpn import AzureVpn
from .vpn.gcp_vpn import GcpVpn
from .vpc.aws_vpc import AwsVpcComponent
from .vpc.azure_vpc import AzureVpcComponent
from .vpc.gcp_vpc import GcpVpcComponent


class SupportedProviders:
    """Enumeración de proveedores soportados."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class VpnProviderFactory:
    """Fábrica para la creación de componentes VPN."""

    # Mapeo de proveedores a sus clases de implementación (OCP)
    _PROVIDERS: Dict[str, Type[VpnComponent]] = {
        SupportedProviders.AWS: AwsVpn,
        SupportedProviders.AZURE: AzureVpn,
        SupportedProviders.GCP: GcpVpn,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None) -> VpnComponent:
        """Crea una instancia de un componente VPN basado en el proveedor.
        ...
        """
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        vpn_class = cls._PROVIDERS[provider]
        return vpn_class(name=name, opts=opts)


class VpcProviderFactory:
    """Fábrica para la creación de componentes VPC."""

    # Mapeo de proveedores a sus clases de implementación (OCP)
    _PROVIDERS = {
        SupportedProviders.AWS: AwsVpcComponent,
        SupportedProviders.AZURE: AzureVpcComponent,
        SupportedProviders.GCP: GcpVpcComponent,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        """Crea una instancia de un componente VPC basado en el proveedor."""
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        vpc_class = cls._PROVIDERS[provider]
        return vpc_class(name=name, opts=opts)

