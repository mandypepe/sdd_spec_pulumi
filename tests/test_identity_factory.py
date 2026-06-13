import pytest
from infra.identity.factory import IdentityProviderFactory
from infra.identity.aws_identity import AwsIdentityComponent
from infra.identity.azure_identity import AzureIdentityComponent
from infra.identity.gcp_identity import GcpIdentityComponent

def test_identity_provider_factory_aws():
    """
    🇪🇸 Prueba la creación del proveedor AWS.
    🇺🇸 Tests AWS provider creation.
    """
    provider = IdentityProviderFactory.create("aws", "test-aws-identity")
    assert isinstance(provider, AwsIdentityComponent)
    assert provider.get_token_endpoint() == "https://sts.amazonaws.com"

def test_identity_provider_factory_azure():
    """
    🇪🇸 Prueba la creación del proveedor Azure.
    🇺🇸 Tests Azure provider creation.
    """
    provider = IdentityProviderFactory.create("azure", "test-azure-identity")
    assert isinstance(provider, AzureIdentityComponent)
    assert provider.get_token_endpoint() == "https://login.microsoftonline.com"

def test_identity_provider_factory_gcp():
    """
    🇪🇸 Prueba la creación del proveedor GCP.
    🇺🇸 Tests GCP provider creation.
    """
    provider = IdentityProviderFactory.create("gcp", "test-gcp-identity")
    assert isinstance(provider, GcpIdentityComponent)
    assert provider.get_token_endpoint() == "https://sts.googleapis.com"

def test_identity_provider_factory_unknown():
    """
    🇪🇸 Prueba el error de proveedor desconocido.
    🇺🇸 Tests unknown provider error.
    """
    with pytest.raises(ValueError, match="Unknown identity provider"):
        IdentityProviderFactory.create("unknown", "test-unknown")
