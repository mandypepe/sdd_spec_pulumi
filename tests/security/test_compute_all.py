import pulumi
from infra.security.factory import SecurityProviderFactory

@pulumi.runtime.test
def test_aws_compute_perimeter():
    component = SecurityProviderFactory.create("aws", "test-compute", "compute")
    assert component.tier == "compute"

@pulumi.runtime.test
def test_azure_compute_perimeter():
    component = SecurityProviderFactory.create("azure", "test-compute", "compute")
    assert component.tier == "compute"

@pulumi.runtime.test
def test_gcp_compute_perimeter():
    component = SecurityProviderFactory.create("gcp", "test-compute", "compute")
    assert component.tier == "compute"
