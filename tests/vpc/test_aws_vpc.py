"""
🇪🇸 Pruebas unitarias para el componente AWS VPC (ComponentResource Testing).
Valida la creación de recursos de red en AWS.

🇺🇸 Unit tests for AWS VPC component (ComponentResource Testing).
Validates AWS network resource creation.
"""

import pulumi
import pytest
from infra.vpc.aws_vpc import AwsVpcComponent


@pulumi.runtime.test
def test_aws_vpc_resources(pulumi_mocks):
    """
    🇪🇸 Verifica que se crean los recursos correctos en AWS VPC.
    Valida que el VPC ID se retorna como output.
    
    🇺🇸 Verify correct resource creation in AWS VPC.
    Validates that VPC ID is returned as output.
    """
    vpc = AwsVpcComponent("test-aws-vpc")
    
    def check_vpc(vpc_id):
        """
        🇪🇸 Función de validación del ID del VPC.
        🇺🇸 VPC ID validation function.
        """
        assert vpc_id == "test-aws-vpc-vpc_id", f"Expected 'test-aws-vpc-vpc_id', got {vpc_id}"
        
    return vpc.vpc_id.apply(check_vpc)
