import pytest
import pulumi
from infra.lb.gcp_lb import GcpLb

@pytest.fixture
def vpc_id():
    return "vpc-12345"

@pytest.fixture
def public_subnet_ids():
    return ["subnet-1", "subnet-2"]

def test_gcp_lb_creation(pulumi_mocks, vpc_id, public_subnet_ids):
    lb = GcpLb("test-gcp-lb", vpc_id, public_subnet_ids)
    
    def check_lb(args):
        name, inputs, urn = args
        assert name == "test-gcp-lb-forwarding-rule"
        assert inputs["load_balancing_scheme"] == "EXTERNAL_MANAGED"
        assert inputs["delete_protection"] == True

    def check_ssl_policy(args):
        name, inputs, urn = args
        assert inputs["min_tls_version"] == "TLS_1_2"
        assert inputs["profile"] == "MODERN"

    def check_health_check(args):
        name, inputs, urn = args
        assert inputs["check_interval_sec"] == 15
        assert inputs["http_health_check"]["request_path"] == "/healthz"

    pulumi.Output.all(lb.lb_arn_or_id).apply(check_lb)
