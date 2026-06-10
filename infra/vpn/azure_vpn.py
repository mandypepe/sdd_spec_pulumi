"""
🇪🇸 Implementación de VPN en Azure siguiendo principios SOLID.
Crea un Resource Group, Virtual Network y Gateway VPN.

🇺🇸 Azure VPN implementation following SOLID principles.
Creates a Resource Group, Virtual Network, and VPN Gateway.
"""

from typing import Any, Dict
import pulumi
import pulumi_azure_native as azure

from ..config import config
from ..constants import (
    AZURE_VNET_CIDR,
    AZURE_GATEWAY_SUBNET_CIDR,
    AZURE_GATEWAY_SUBNET_NAME,
    AZURE_VPN_SKU,
)
from .base import VpnComponent


class AzureVpn(VpnComponent):
    """Componente VPN para Azure."""

    def __init__(self, name: str, opts: pulumi.ResourceOptions | None = None):
        super().__init__("infra:azure:Vpn", name, opts)

        # Resource Group
        self.resource_group = azure.resources.ResourceGroup(
            resource_name=f"{name}-rg",
            resource_group_name=f"{name}-rg",
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Virtual Network
        self.vnet = azure.network.VirtualNetwork(
            resource_name=f"{name}-vnet",
            resource_group_name=self.resource_group.name,
            address_space=azure.network.AddressSpaceArgs(address_prefixes=[AZURE_VNET_CIDR]),
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Public IP para el gateway
        self.public_ip = azure.network.PublicIPAddress(
            resource_name=f"{name}-gw-pip",
            resource_group_name=self.resource_group.name,
            public_ip_allocation_method=azure.network.IPAllocationMethod.DYNAMIC,
            sku=azure.network.PublicIPAddressSkuArgs(name="Basic"),
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Gateway Subnet
        self.gateway_subnet = azure.network.Subnet(
            resource_name=f"{name}-gateway-subnet",
            resource_group_name=self.resource_group.name,
            virtual_network_name=self.vnet.name,
            subnet_name=AZURE_GATEWAY_SUBNET_NAME,
            address_prefix=AZURE_GATEWAY_SUBNET_CIDR,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Virtual Network Gateway
        self.vpn_gateway = azure.network.VirtualNetworkGateway(
            resource_name=f"{name}-vnet-gateway",
            resource_group_name=self.resource_group.name,
            virtual_network_gateway_name=f"{name}-vnet-gateway",
            sku=azure.network.VirtualNetworkGatewaySkuArgs(name=AZURE_VPN_SKU, tier=AZURE_VPN_SKU),
            gateway_type=azure.network.VirtualNetworkGatewayType.VPN,
            vpn_type=azure.network.VpnType.ROUTE_BASED,
            ip_configurations=[
                azure.network.VirtualNetworkGatewayIPConfigurationArgs(
                    name="vnetGatewayConfig",
                    public_ip_address=azure.network.SubResourceArgs(id=self.public_ip.id),
                    subnet=azure.network.SubResourceArgs(id=self.gateway_subnet.id),
                )
            ],
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.register_outputs(self.get_outputs())

    def get_outputs(self) -> Dict[str, Any]:
        """Salidas públicas del componente Azure."""
        return {
            "resource_group": self.resource_group.name,
            "vnet_id": self.vnet.id,
            "vpn_gateway_id": self.vpn_gateway.id,
        }

