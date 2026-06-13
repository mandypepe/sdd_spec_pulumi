import pulumi
from infra.security.factory import SecurityProviderFactory

@pulumi.runtime.test
def test_gcp_public_perimeter():
    component = SecurityProviderFactory.create("gcp", "test-public", "public")
    assert component.tier == "public"
