"""
🇪🇸 Implementación de VPN en AWS siguiendo principios SOLID.
Crea recursos de red mínimos necesarios para una VPN.

🇺🇸 AWS VPN implementation following SOLID principles.
Creates minimal network resources required for a VPN.
"""

from typing import Any, Dict
import pulumi
import pulumi_aws as aws

from ..config import config
from ..constants import AWS_VPC_CIDR
from .base import VpnComponent


class AwsVpn(VpnComponent):
    """Componente VPN para AWS."""

    def __init__(self, name: str, opts: pulumi.ResourceOptions | None = None):
        super().__init__("infra:aws:Vpn", name, opts)

        # VPC: Aislamiento de red
        self.vpc = aws.ec2.Vpc(
            resource_name=f"{name}-vpc",
            cidr_block=AWS_VPC_CIDR,
            tags={**config.tags, "Name": f"{name}-vpc"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Internet Gateway: Acceso a red
        self.igw = aws.ec2.InternetGateway(
            resource_name=f"{name}-igw",
            vpc_id=self.vpc.id,
            tags={**config.tags, "Name": f"{name}-igw"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        # VPN Gateway
        self.vpn_gateway = aws.ec2.VpnGateway(
            resource_name=f"{name}-vpn-gateway",
            vpc_id=self.vpc.id,
            tags={**config.tags, "Name": f"{name}-vpn-gateway"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.register_outputs(self.get_outputs())

    def get_outputs(self) -> Dict[str, Any]:
        """Salidas públicas del componente AWS."""
        return {
            "vpc_id": self.vpc.id,
            "vpn_gateway_id": self.vpn_gateway.id,
        }

