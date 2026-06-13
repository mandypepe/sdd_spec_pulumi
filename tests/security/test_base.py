import pytest
import pulumi
from infra.security.factory import SecurityProviderFactory

@pulumi.runtime.test
def test_security_factory_creation():
    # Test factory creation for supported providers (mocked)
    for provider in ["aws", "azure", "gcp"]:
        component = SecurityProviderFactory.create(provider, "test", "public")
        assert component is not None
        assert component.tier == "public"

def test_unsupported_provider():
    with pytest.raises(ValueError):
        SecurityProviderFactory.create("unsupported", "test", "public")
