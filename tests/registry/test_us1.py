import pytest
import pulumi
from infra.registry.aws_registry import AwsRegistry
from infra.registry.azure_registry import AzureRegistry
from infra.registry.gcp_registry import GcpRegistry

@pulumi.runtime.test
def test_aws_registry_provisioning():
    def check_id(args):
        assert args == "aws-ecr-id"
    
    registry = AwsRegistry("test-aws", "us-east-1")
    return registry.registry_id.apply(check_id)

@pulumi.runtime.test
def test_azure_registry_provisioning():
    def check_id(args):
        assert args == "azure-acr-id"
    
    registry = AzureRegistry("test-azure", "eastus")
    return registry.registry_id.apply(check_id)

@pulumi.runtime.test
def test_gcp_registry_provisioning():
    def check_id(args):
        assert args == "gcp-gar-id"
    
    registry = GcpRegistry("test-gcp", "us-central1")
    return registry.registry_id.apply(check_id)
