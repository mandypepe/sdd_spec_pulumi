import pytest
import pulumi
from infra.lb.azure_lb import AzureLb

@pytest.fixture
def vpc_id():
    return "vpc-12345"

@pytest.fixture
def public_subnet_ids():
    return ["subnet-1", "subnet-2"]

def test_azure_lb_creation(pulumi_mocks, vpc_id, public_subnet_ids):
    lb = AzureLb("test-azure-lb", vpc_id, public_subnet_ids)
    
    def check_lb(args):
        name, inputs, urn = args
        assert name == "test-azure-lb-appgw"
        assert inputs["sku"]["name"] == "Standard_v2"
        # Verify TLS 1.3 in SSL Policy
        if "ssl_policy" in inputs:
            assert inputs["ssl_policy"]["min_protocol_version"] == "TLSv1_3"
        # Verify Health Probes
        if "probes" in inputs:
            assert inputs["probes"][0]["interval"] == 15
            assert inputs["probes"][0]["path"] == "/healthz"

    pulumi.Output.all(lb.lb_arn_or_id).apply(check_lb)
