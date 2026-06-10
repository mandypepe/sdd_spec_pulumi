"""
🇪🇸 Pruebas unitarias para la Factory de proveedores VPN (Factory Pattern Testing).
Valida que la Factory cree las instancias correctas para cada proveedor.

🇺🇸 Unit tests for VPN provider Factory (Factory Pattern Testing).
Validates that Factory creates correct instances for each provider.
"""

import pytest
from infra.providers import VpnProviderFactory, SupportedProviders
from infra.vpn.aws_vpn import AwsVpn
from infra.vpn.azure_vpn import AzureVpn
from infra.vpn.gcp_vpn import GcpVpn


def test_factory_creates_aws_vpn(pulumi_mocks):
    """
    🇪🇸 Verifica que la Factory cree una instancia correcta de AwsVpn.
    Valida que el nombre del recurso se asigne correctamente.
    
    🇺🇸 Verifies Factory creates correct AwsVpn instance.
    Validates that resource name is assigned correctly.
    """
    vpn = VpnProviderFactory.create("aws", "test-aws")
    assert isinstance(vpn, AwsVpn), f"Expected AwsVpn instance, got {type(vpn)}"
    assert vpn.resource_name == "test-aws", f"Expected resource_name 'test-aws', got {vpn.resource_name}"


def test_factory_creates_azure_vpn(pulumi_mocks):
    """
    🇪🇸 Verifica que la Factory cree una instancia correcta de AzureVpn.
    
    🇺🇸 Verifies Factory creates correct AzureVpn instance.
    """
    vpn = VpnProviderFactory.create("azure", "test-azure")
    assert isinstance(vpn, AzureVpn), f"Expected AzureVpn instance, got {type(vpn)}"
    assert vpn.resource_name == "test-azure", f"Expected resource_name 'test-azure', got {vpn.resource_name}"


def test_factory_creates_gcp_vpn(pulumi_mocks):
    """
    🇪🇸 Verifica que la Factory cree una instancia correcta de GcpVpn.
    
    🇺🇸 Verifies Factory creates correct GcpVpn instance.
    """
    vpn = VpnProviderFactory.create("gcp", "test-gcp")
    assert isinstance(vpn, GcpVpn), f"Expected GcpVpn instance, got {type(vpn)}"
    assert vpn.resource_name == "test-gcp", f"Expected resource_name 'test-gcp', got {vpn.resource_name}"


def test_factory_raises_error_on_invalid_provider(pulumi_mocks):
    """
    🇪🇸 Verifica que la Factory lance un error (ValueError) con un proveedor inválido.
    Valida el comportamiento de error de la Factory.
    
    🇺🇸 Verifies Factory raises error (ValueError) for invalid provider.
    Validates Factory error handling behavior.
    """
    with pytest.raises(ValueError, match="Unsupported provider"):
        VpnProviderFactory.create("invalid-cloud", "test-fail")
