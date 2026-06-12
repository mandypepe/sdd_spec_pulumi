import pytest
import pulumi
from infra.providers import LbProviderFactory, SupportedProviders
from infra.lb.aws_lb import AwsLb
from infra.lb.azure_lb import AzureLb
from infra.lb.gcp_lb import GcpLb

@pytest.fixture
def vpc_id():
    return "vpc-12345"

@pytest.fixture
def public_subnet_ids():
    return ["subnet-1", "subnet-2"]

def test_lb_factory_aws(pulumi_mocks, vpc_id, public_subnet_ids):
    lb = LbProviderFactory.create(SupportedProviders.AWS, "test-aws-lb", vpc_id, public_subnet_ids)
    assert isinstance(lb, AwsLb)
    assert lb.vpc_id == vpc_id
    assert lb.public_subnet_ids == public_subnet_ids

def test_lb_factory_azure(pulumi_mocks, vpc_id, public_subnet_ids):
    lb = LbProviderFactory.create(SupportedProviders.AZURE, "test-azure-lb", vpc_id, public_subnet_ids)
    assert isinstance(lb, AzureLb)
    assert lb.vpc_id == vpc_id
    assert lb.public_subnet_ids == public_subnet_ids

def test_lb_factory_gcp(pulumi_mocks, vpc_id, public_subnet_ids):
    lb = LbProviderFactory.create(SupportedProviders.GCP, "test-gcp-lb", vpc_id, public_subnet_ids)
    assert isinstance(lb, GcpLb)
    assert lb.vpc_id == vpc_id
    assert lb.public_subnet_ids == public_subnet_ids

def test_lb_factory_invalid_provider(pulumi_mocks, vpc_id, public_subnet_ids):
    with pytest.raises(ValueError, match="Unsupported provider: 'invalid'"):
        LbProviderFactory.create("invalid", "test-invalid-lb", vpc_id, public_subnet_ids)
