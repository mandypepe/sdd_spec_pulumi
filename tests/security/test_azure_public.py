import pulumi
from infra.security.factory import SecurityProviderFactory

@pulumi.runtime.test
def test_azure_public_perimeter():
    component = SecurityProviderFactory.create("azure", "test-public", "public")
    assert component.tier == "public"
