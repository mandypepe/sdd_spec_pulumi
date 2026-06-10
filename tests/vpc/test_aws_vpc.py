import pulumi
import pytest
from infra.vpc.aws_vpc import AwsVpcComponent

@pulumi.runtime.test
def test_aws_vpc_resources(pulumi_mocks):
    """
    🇪🇸 Verifica que se crean los recursos correctos en AWS VPC.
    🇺🇸 Verify correct resource creation in AWS VPC.
    """
    vpc = AwsVpcComponent("test-aws-vpc")
    
    def check_vpc(vpc_id):
        assert vpc_id == "test-aws-vpc-vpc_id"
        
    return vpc.vpc_id.apply(check_vpc)
