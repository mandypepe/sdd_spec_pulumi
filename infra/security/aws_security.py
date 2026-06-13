import pulumi
import pulumi_aws as aws
from .base import SecurityComponent
from ..config import config
from typing import Optional

class AwsSecurity(SecurityComponent):
    def __init__(self, resource_type: str, name: str, tier: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__(resource_type, name, tier, opts=opts)
        self.name = name
        self._create_firewall_rules()
        self._configure_logging()
        
    def _create_firewall_rules(self):
        # FR-002: HTTPS for Public Tier
        if self.tier == "public":
            aws.ec2.SecurityGroup(
                f"{self.name}-sg",
                description="Public HTTPS access",
                ingress=[aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=443,
                    to_port=443,
                    cidr_blocks=["0.0.0.0/0"]
                )],
                opts=pulumi.ResourceOptions(parent=self)
            )
        # FR-004 & FR-007: Compute Tier SSH Block and Outbound Whitelist
        elif self.tier == "compute":
            aws.ec2.SecurityGroup(
                f"{self.name}-sg",
                description="Compute tier isolation",
                ingress=[aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=22,
                    to_port=22,
                    cidr_blocks=["10.0.0.0/16"], 
                    description="Internal access only"
                )],
                egress=[aws.ec2.SecurityGroupEgressArgs(
                    protocol="tcp",
                    from_port=443,
                    to_port=443,
                    cidr_blocks=["1.2.3.4/32"],
                    description="Whitelist domains only"
                )],
                opts=pulumi.ResourceOptions(parent=self, protect=True)
            )
        # FR-005 & FR-006: Data Tier Isolation
        elif self.tier == "data":
            aws.ec2.SecurityGroup(
                f"{self.name}-sg",
                description="Data tier isolation",
                ingress=[aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=5432,
                    to_port=5432,
                    cidr_blocks=["10.0.10.0/23"], # Private compute
                    description="Postgres from compute only"
                )],
                egress=[], # FR-006: Explicit Deny All Outbound
                opts=pulumi.ResourceOptions(parent=self, protect=True)
            )

    def _configure_logging(self):
        # FR-009: 365 days
        aws.cloudwatch.LogGroup(
            f"{self.name}-log",
            retention_in_days=config.security_log_retention_days,
            opts=pulumi.ResourceOptions(parent=self)
        )
