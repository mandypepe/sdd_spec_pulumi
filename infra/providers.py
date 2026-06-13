"""
🇪🇸 Factory para seleccionar los proveedores de infraestructura (Factory Pattern & Open/Closed Principle).
Permite extensión de proveedores sin modificar la lógica central.

🇺🇸 Factory for selecting infrastructure providers (Factory Pattern & Open/Closed Principle).
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
from .lb.base import LbComponent
from .lb.aws_lb import AwsLb
from .lb.azure_lb import AzureLb
from .lb.gcp_lb import GcpLb
from .registry.base import RegistryComponent
from .registry.aws_registry import AwsRegistry
from .registry.azure_registry import AzureRegistry
from .registry.gcp_registry import GcpRegistry
from .db.base import DatabaseComponent
from .db.aws_db import AwsDatabase
from .db.azure_db import AzureDatabase
from .db.gcp_db import GcpDatabase


class SupportedProviders:
    """
    🇪🇸 Enumeración de proveedores soportados.
    
    🇺🇸 Enumeration of supported cloud providers.
    """
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class RegistryProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes de Registro.
    🇺🇸 Factory for Registry component creation.
    """

    _PROVIDERS: Dict[str, Type[RegistryComponent]] = {
        SupportedProviders.AWS: AwsRegistry,
        SupportedProviders.AZURE: AzureRegistry,
        SupportedProviders.GCP: GcpRegistry,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, region: str, opts: Optional[pulumi.ResourceOptions] = None) -> RegistryComponent:
        provider = (provider_name or "").lower()
        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(f"Unsupported provider: '{provider_name}'. Supported: {supported}")
        
        registry_class = cls._PROVIDERS[provider]
        return registry_class(name=name, region=region, opts=opts)


class VpnProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes VPN.
    🇺🇸 Factory for VPN component creation.
    """

    _PROVIDERS: Dict[str, Type[VpnComponent]] = {
        SupportedProviders.AWS: AwsVpn,
        SupportedProviders.AZURE: AzureVpn,
        SupportedProviders.GCP: GcpVpn,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None) -> VpnComponent:
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
    🇪🇸 Factory para la creación de componentes VPC.
    🇺🇸 Factory for VPC component creation.
    """

    _PROVIDERS = {
        SupportedProviders.AWS: AwsVpcComponent,
        SupportedProviders.AZURE: AzureVpcComponent,
        SupportedProviders.GCP: GcpVpcComponent,
    }

    @classmethod
    def create(cls, provider_name: str, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        vpc_class = cls._PROVIDERS[provider]
        return vpc_class(name=name, opts=opts)


class LbProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes de Load Balancer.
    🇺🇸 Factory for Load Balancer component creation.
    """

    _PROVIDERS = {
        SupportedProviders.AWS: AwsLb,
        SupportedProviders.AZURE: AzureLb,
        SupportedProviders.GCP: GcpLb,
    }

    @classmethod
    def create(
        cls, 
        provider_name: str, 
        name: str, 
        vpc_id: pulumi.Input[str],
        public_subnet_ids: pulumi.Input[list[str]],
        opts: Optional[pulumi.ResourceOptions] = None
    ) -> LbComponent:
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        lb_class = cls._PROVIDERS[provider]
        return lb_class(name=name, vpc_id=vpc_id, public_subnet_ids=public_subnet_ids, opts=opts)


class DatabaseProviderFactory:
    """
    🇪🇸 Factory para la creación de componentes de Base de Datos.
    🇺🇸 Factory for Database component creation.
    """

    _PROVIDERS: Dict[str, Type[DatabaseComponent]] = {
        SupportedProviders.AWS: AwsDatabase,
        SupportedProviders.AZURE: AzureDatabase,
        SupportedProviders.GCP: GcpDatabase,
    }

    @classmethod
    def create(
        cls,
        provider_name: str,
        name: str,
        opts: Optional[pulumi.ResourceOptions] = None
    ) -> DatabaseComponent:
        provider = (provider_name or "").lower()

        if provider not in cls._PROVIDERS:
            supported = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported provider: '{provider_name}'. Supported: {supported}"
            )

        db_class = cls._PROVIDERS[provider]
        return db_class(name=name, opts=opts)
