from .base import LbComponent
import pulumi
import pulumi_azure_native.network as network
from typing import Optional, List
from ..config import config

class AzureLb(LbComponent):
    def __init__(
        self, 
        name: str, 
        vpc_id: pulumi.Input[str], 
        public_subnet_ids: pulumi.Input[List[str]], 
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        super().__init__("infra:azure:Lb", name, vpc_id, public_subnet_ids, opts)
        
        self._create_load_balancer()
        
        self.register_outputs({
            "dns_name": self.dns_name,
            "lb_arn_or_id": self.lb_arn_or_id,
            "security_group_id": self.security_group_id
        })

    def _create_load_balancer(self):
        self.app_gw = network.ApplicationGateway(
            f"{self._name}-appgw",
            resource_group_name="placeholder-rg",
            location="eastus",
            sku=network.ApplicationGatewaySkuArgs(
                name="Standard_v2",
                tier="Standard_v2",
                capacity=2,
            ),
            ssl_policy=network.ApplicationGatewaySslPolicyArgs(
                policy_type="CustomV2",
                min_protocol_version="TLSv1_3",
            ),
            gateway_ip_configurations=[network.ApplicationGatewayIPConfigurationArgs(
                name="appGatewayIpConfig",
                subnet=network.SubResourceArgs(id=self.public_subnet_ids[0]),
            )],
            frontend_ports=[network.ApplicationGatewayFrontendPortArgs(
                name="port_443",
                port=443,
            )],
            probes=[network.ApplicationGatewayProbeArgs(
                name="customProbe",
                protocol="Https",
                path=config.lb_health_check_path,
                interval=config.lb_health_check_interval,
                timeout=10,
                unhealthy_threshold=3,
                pick_host_name_from_backend_http_settings=True,
            )],
            opts=pulumi.ResourceOptions(parent=self, protect=config.lb_enable_deletion_protection)
        )
        
        self.dns_name = self.app_gw.name
        self.lb_arn_or_id = self.app_gw.id
        self.security_group_id = pulumi.Output.from_input("nsg-id")

    def _create_listener(self, certificate_arn_or_id: str):
        pass

    def _create_target_group(self):
        pass
