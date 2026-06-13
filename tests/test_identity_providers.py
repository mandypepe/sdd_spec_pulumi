import pytest
from infra.identity.aws_identity import AwsIdentityComponent
from infra.identity.azure_identity import AzureIdentityComponent
from infra.identity.gcp_identity import GcpIdentityComponent

def test_aws_identity_boundary():
    """
    🇪🇸 Prueba la política de límites de AWS.
    🇺🇸 Tests AWS boundary policy.
    """
    provider = AwsIdentityComponent("test-aws")
    # This should not raise an exception
    provider.apply_boundary_policy("arn:aws:iam::123456789012:policy/boundary")

def test_azure_identity_boundary():
    """
    🇪🇸 Prueba la política de límites de Azure.
    🇺🇸 Tests Azure boundary policy.
    """
    provider = AzureIdentityComponent("test-azure")
    # This should not raise an exception
    provider.apply_boundary_policy("role-definition-id")

def test_gcp_identity_boundary():
    """
    🇪🇸 Prueba la política de límites de GCP.
    🇺🇸 Tests GCP boundary policy.
    """
    provider = GcpIdentityComponent("test-gcp")
    # This should not raise an exception
    provider.apply_boundary_policy("projects/my-project/locations/global/workloadIdentityPools/my-pool")
