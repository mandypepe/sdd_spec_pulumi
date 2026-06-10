"""Implementaciones del componente VPN por proveedor.

Cada archivo define una clase ComponentResource que implementa la creación
de los recursos necesarios para proporcionar una VPN básica en el proveedor
correspondiente.
"""

from .base import VpnComponent
from .aws_vpn import AwsVpn
from .azure_vpn import AzureVpn
from .gcp_vpn import GcpVpn

__all__ = ["VpnComponent", "AwsVpn", "AzureVpn", "GcpVpn"]

