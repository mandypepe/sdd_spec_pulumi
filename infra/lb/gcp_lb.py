from .base import LbComponent
import pulumi
import pulumi_gcp as gcp
from typing import Optional, List
from ..config import config

class GcpLb(LbComponent):
    def __init__(
        self, 
        name: str, 
        vpc_id: pulumi.Input[str], 
        public_subnet_ids: pulumi.Input[List[str]], 
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        super().__init__("infra:gcp:Lb", name, vpc_id, public_subnet_ids, opts)
        
        self._create_load_balancer()
        
        self.register_outputs({
            "dns_name": self.dns_name,
            "lb_arn_or_id": self.lb_arn_or_id,
            "security_group_id": self.security_group_id
        })

    def _create_load_balancer(self):
        # SSL Policy for TLS 1.3
        self.ssl_policy = gcp.compute.SSLPolicy(
            f"{self._name}-ssl-policy",
            min_tls_version="TLS_1_2",
            profile="MODERN",
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Health Check
        self.health_check = gcp.compute.HealthCheck(
            f"{self._name}-health-check",
            check_interval_sec=config.lb_health_check_interval,
            http_health_check=gcp.compute.HealthCheckHttpHealthCheckArgs(
                port=80,
                request_path=config.lb_health_check_path,
            ),
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Backend Service
        self.backend_service = gcp.compute.BackendService(
            f"{self._name}-backend",
            protocol="HTTP",
            load_balancing_scheme="EXTERNAL_MANAGED",
            health_checks=self.health_check.id,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # URL Map
        self.url_map = gcp.compute.URLMap(
            f"{self._name}-url-map",
            default_service=self.backend_service.id,
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Target HTTPS Proxy
        self.target_proxy = gcp.compute.TargetHttpsProxy(
            f"{self._name}-https-proxy",
            url_map=self.url_map.id,
            ssl_certificates=[config.lb_certificate_arn_or_id or "dummy-cert"],
            ssl_policy=self.ssl_policy.id,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Forwarding Rule
        self.forwarding_rule = gcp.compute.GlobalForwardingRule(
            f"{self._name}-forwarding-rule",
            load_balancing_scheme="EXTERNAL_MANAGED",
            port_range="443",
            target=self.target_proxy.id,
            opts=pulumi.ResourceOptions(parent=self, protect=config.lb_enable_deletion_protection)
        )
        
        self.dns_name = self.forwarding_rule.ip_address
        self.lb_arn_or_id = self.forwarding_rule.id
        self.security_group_id = pulumi.Output.from_input("firewall-id")

    def _create_listener(self, certificate_arn_or_id: str):
        pass

    def _create_target_group(self):
        pass
