"""Pruebas unitarias para la fábrica de proveedores VPN."""

import pytest
from infra.providers import VpnProviderFactory, SupportedProviders
from infra.vpn.aws_vpn import AwsVpn
from infra.vpn.azure_vpn import AzureVpn
from infra.vpn.gcp_vpn import GcpVpn


def test_factory_creates_aws_vpn(pulumi_mocks):
    """Verifica que la fábrica cree una instancia de AwsVpn."""
    vpn = VpnProviderFactory.create("aws", "test-aws")
    assert isinstance(vpn, AwsVpn)
    assert vpn.resource_name == "test-aws"


def test_factory_creates_azure_vpn(pulumi_mocks):
    """Verifica que la fábrica cree una instancia de AzureVpn."""
    vpn = VpnProviderFactory.create("azure", "test-azure")
    assert isinstance(vpn, AzureVpn)
    assert vpn.resource_name == "test-azure"


def test_factory_creates_gcp_vpn(pulumi_mocks):
    """Verifica que la fábrica cree una instancia de GcpVpn."""
    vpn = VpnProviderFactory.create("gcp", "test-gcp")
    assert isinstance(vpn, GcpVpn)
    assert vpn.resource_name == "test-gcp"


def test_factory_raises_error_on_invalid_provider(pulumi_mocks):
    """Verifica que la fábrica lance un error con un proveedor inválido."""
    with pytest.raises(ValueError, match="Unsupported provider"):
        VpnProviderFactory.create("invalid-cloud", "test-fail")
