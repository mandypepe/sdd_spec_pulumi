"""
🇪🇸 Factory para seleccionar el proveedor VPN (Factory Pattern & Open/Closed Principle).
Permite extensión de proveedores sin modificar la lógica central.

🇺🇸 Factory for selecting the VPN provider (Factory Pattern & Open/Closed Principle).
Enables provider extension without modifying core logic.
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
    """
    🇪🇸 Enumeración de proveedores soportados.
    
    🇺🇸 Enumeration of supported cloud providers.
    """
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class VpnProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes VPN (Factory Pattern).
    Mapea nombres de proveedor a implementaciones concretas.
    
    🇺🇸 Factory for VPN component creation (Factory Pattern).
    Maps provider names to concrete implementations.
    """

    # Mapeo de proveedores a sus clases (Open/Closed Principle)
    _PROVIDERS: Dict[str, Type[VpnComponent]] = {
        SupportedProviders.AWS: AwsVpn,
        SupportedProviders.AZURE: AzureVpn,
        SupportedProviders.GCP: GcpVpn,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None) -> VpnComponent:
        """
        🇪🇸 Crea una instancia de un componente VPN según el proveedor solicitado.
        
        🇺🇸 Creates a VPN component instance for the requested provider.
        
        Args:
            provider_name: 🇪🇸 Nombre del proveedor ('aws', 'azure', 'gcp') / 🇺🇸 Provider name ('aws', 'azure', 'gcp')
            name: 🇪🇸 Nombre base del recurso / 🇺🇸 Base resource name
            opts: 🇪🇸 Opciones de Pulumi / 🇺🇸 Pulumi ResourceOptions
            
        Returns:
            🇪🇸 Instancia del componente VPN / 🇺🇸 VPN component instance
            
        Raises:
            ValueError: 🇪🇸 Si el proveedor no es soportado / 🇺🇸 If provider is unsupported
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
    """
    🇪🇸 Factory para la creación de componentes VPC (Factory Pattern).
    Mapea nombres de proveedor a implementaciones concretas.
    
    🇺🇸 Factory for VPC component creation (Factory Pattern).
    Maps provider names to concrete implementations.
    """

    # Mapeo de proveedores a sus clases (Open/Closed Principle)
    _PROVIDERS = {
        SupportedProviders.AWS: AwsVpcComponent,
        SupportedProviders.AZURE: AzureVpcComponent,
        SupportedProviders.GCP: GcpVpcComponent,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        """
        🇪🇸 Crea una instancia de un componente VPC según el proveedor solicitado.
        
        🇺🇸 Creates a VPC component instance for the requested provider.
        
        Args:
            provider_name: 🇪🇸 Nombre del proveedor ('aws', 'azure', 'gcp') / 🇺🇸 Provider name ('aws', 'azure', 'gcp')
            name: 🇪🇸 Nombre base del recurso / 🇺🇸 Base resource name
            opts: 🇪🇸 Opciones de Pulumi / 🇺🇸 Pulumi ResourceOptions
            
        Returns:
            🇪🇸 Instancia del componente VPC / 🇺🇸 VPC component instance
            
        Raises:
            ValueError: 🇪🇸 Si el proveedor no es soportado / 🇺🇸 If provider is unsupported
        """
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        vpc_class = cls._PROVIDERS[provider]
        return vpc_class(name=name, opts=opts)

