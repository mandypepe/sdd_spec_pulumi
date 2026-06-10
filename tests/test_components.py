"""Pruebas unitarias para validar la creación de recursos en los componentes."""

import pulumi
import pytest
from infra.vpn.aws_vpn import AwsVpn
from infra.constants import AWS_VPC_CIDR


@pulumi.runtime.test
def test_aws_vpn_resources(pulumi_mocks):
    """Verifica que el componente AWS cree los recursos con los parámetros correctos."""
    name = "my-aws-vpn"
    aws_vpn = AwsVpn(name)

    def check_vpc(args):
        # Los recursos de Pulumi no exponen el nombre de entrada directamente de forma obvia en Output
        # pero podemos verificar el CIDR y los tags que enviamos.
        cidr, tags = args
        assert cidr == AWS_VPC_CIDR
        assert tags["project"] == "multi-cloud-vpn"

    # Verificación asíncrona de las salidas de Pulumi
    return pulumi.Output.all(aws_vpn.vpc.cidr_block, aws_vpn.vpc.tags).apply(check_vpc)
