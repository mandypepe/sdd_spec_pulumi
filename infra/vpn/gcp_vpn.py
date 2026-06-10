"""
🇪🇸 Implementación de VPN en GCP siguiendo principios SOLID.
Crea una VPC, subred y VPN Gateway.

🇺🇸 GCP VPN implementation following SOLID principles.
Creates a VPC, subnet, and VPN Gateway.
"""

from typing import Any, Dict
import pulumi
import pulumi_gcp as gcp

from ..config import config
from ..constants import GCP_NETWORK_CIDR, GCP_DEFAULT_REGION
from .base import VpnComponent


class GcpVpn(VpnComponent):
    """Componente VPN para GCP."""

    def __init__(self, name: str, opts: pulumi.ResourceOptions | None = None):
        super().__init__("infra:gcp:Vpn", name, opts)

        # Network (VPC)
        self.network = gcp.compute.Network(
            resource_name=f"{name}-network",
            name=f"{name}-network",
            auto_create_subnetworks=False,
            description="VPC for example vpn",
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Subnetwork
        self.subnet = gcp.compute.Subnetwork(
            resource_name=f"{name}-subnet",
            name=f"{name}-subnet",
            ip_cidr_range=GCP_NETWORK_CIDR,
            region=config.gcp_region or GCP_DEFAULT_REGION,
            network=self.network.id,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # VPN Gateway
        self.vpn_gateway = gcp.compute.VPNGateway(
            resource_name=f"{name}-vpn-gateway",
            network=self.network.id,
            region=config.gcp_region or GCP_DEFAULT_REGION,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.register_outputs(self.get_outputs())

    def get_outputs(self) -> Dict[str, Any]:
        """Salidas públicas del componente GCP."""
        return {
            "network": self.network.name,
            "vpn_gateway": self.vpn_gateway.id,
        }

