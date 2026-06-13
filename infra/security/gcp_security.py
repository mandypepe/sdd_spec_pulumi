import pulumi
import pulumi_gcp as gcp
from .base import SecurityComponent
from typing import Optional

class GcpSecurity(SecurityComponent):
    def __init__(self, resource_type: str, name: str, tier: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__(resource_type, name, tier, opts=opts)
        self.name = name
        self._create_firewall_rules()
        self._configure_logging()
        
    def _create_firewall_rules(self):
        # FR-002: HTTPS for Public Tier
        if self.tier == "public":
            gcp.compute.Firewall(
                f"{self.name}-fw",
                network="dummy",
                allows=[gcp.compute.FirewallAllowArgs(
                    protocol="tcp",
                    ports=["443"]
                )],
                source_ranges=["0.0.0.0/0"],
                opts=pulumi.ResourceOptions(parent=self)
            )

    def _configure_logging(self):
        # FR-009: Placeholder for GCP Logging retention policy
        pass
