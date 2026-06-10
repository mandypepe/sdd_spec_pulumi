"""
🇪🇸 Pruebas unitarias para validar la creación de recursos en componentes VPN.
Verifica que los parámetros y tags se asignen correctamente.

🇺🇸 Unit tests to validate resource creation in VPN components.
Verifies that parameters and tags are assigned correctly.
"""

import pulumi
import pytest
from infra.vpn.aws_vpn import AwsVpn
from infra.constants import AWS_VPC_CIDR


@pulumi.runtime.test
def test_aws_vpn_resources(pulumi_mocks):
    """
    🇪🇸 Verifica que el componente AWS cree los recursos con los parámetros correctos.
    Valida el CIDR y los tags aplicados al VPC.
    
    🇺🇸 Verifies that AWS component creates resources with correct parameters.
    Validates CIDR and tags applied to VPC.
    """
    name = "my-aws-vpn"
    aws_vpn = AwsVpn(name)

    def check_vpc(args):
        """
        🇪🇸 Función de validación de salidas asincrónicas.
        🇺🇸 Validation function for async outputs.
        """
        cidr, tags = args
        assert cidr == AWS_VPC_CIDR, f"Expected CIDR {AWS_VPC_CIDR}, got {cidr}"
        assert tags["project"] == "multi-cloud-vpn", "Missing or incorrect 'project' tag"

    # Verificación asincrónica de las salidas de Pulumi (Async Validation)
    # Asynchronous verification of Pulumi outputs (Async Validation)
    return pulumi.Output.all(aws_vpn.vpc.cidr_block, aws_vpn.vpc.tags).apply(check_vpc)
