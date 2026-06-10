"""Constantes compartidas del módulo infra.

Usar constantes evita valores mágicos y facilita cambios globales.
"""

# Naming y Tags
DEFAULT_VPN_NAME = "vpn"
DEFAULT_TAGS = {"project": "multi-cloud-vpn", "managed-by": "pulumi"}

# CIDR Blocks
AWS_VPC_CIDR = "10.0.0.0/16"
AZURE_VNET_CIDR = "10.1.0.0/16"
AZURE_GATEWAY_SUBNET_CIDR = "10.1.255.0/27"
GCP_NETWORK_CIDR = "10.2.0.0/16"

# Azure Specifics
AZURE_GATEWAY_SUBNET_NAME = "GatewaySubnet"
AZURE_VPN_SKU = "VpnGw1"

# GCP Specifics
GCP_DEFAULT_REGION = "us-central1"

