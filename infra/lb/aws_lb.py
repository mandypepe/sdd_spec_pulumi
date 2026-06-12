from .base import LbComponent
import pulumi
import pulumi_aws as aws
from typing import Optional, List
from ..config import config

class AwsLb(LbComponent):
    def __init__(
        self, 
        name: str, 
        vpc_id: pulumi.Input[str], 
        public_subnet_ids: pulumi.Input[List[str]], 
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        super().__init__("infra:aws:Lb", name, vpc_id, public_subnet_ids, opts)
        
        self._create_load_balancer()
        self._create_target_group()
        
        # In a real scenario, the certificate ARN would come from config
        cert_arn = config.lb_certificate_arn_or_id or "arn:aws:acm:region:account:certificate/dummy"
        self._create_listener(cert_arn)
        
        self.register_outputs({
            "dns_name": self.dns_name,
            "lb_arn_or_id": self.lb_arn_or_id,
            "security_group_id": self.security_group_id
        })

    def _create_load_balancer(self):
        self.security_group = aws.ec2.SecurityGroup(
            f"{self._name}-sg",
            vpc_id=self.vpc_id,
            description="Perimeter traffic filter for LB",
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=443,
                    to_port=443,
                    cidr_blocks=["0.0.0.0/0"],
                    description="Allow HTTPS from internet"
                )
            ],
            egress=[
                aws.ec2.SecurityGroupEgressArgs(
                    protocol="tcp",
                    from_port=config.lb_backend_port_min,
                    to_port=config.lb_backend_port_max,
                    cidr_blocks=["0.0.0.0/0"], # Should be restricted to private compute SG in production
                    description="Allow traffic to backend compute nodes"
                )
            ],
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        self.alb = aws.lb.LoadBalancer(
            f"{self._name}-alb",
            load_balancer_type="application",
            subnets=self.public_subnet_ids,
            security_groups=[self.security_group.id],
            enable_deletion_protection=config.lb_enable_deletion_protection,
            opts=pulumi.ResourceOptions(parent=self, protect=config.lb_enable_deletion_protection)
        )
        
        self.dns_name = self.alb.dns_name
        self.lb_arn_or_id = self.alb.arn
        self.security_group_id = self.security_group.id

    def _create_listener(self, certificate_arn_or_id: str):
        self.listener = aws.lb.Listener(
            f"{self._name}-listener",
            load_balancer_arn=self.alb.arn,
            port=443,
            protocol="HTTPS",
            ssl_policy="ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
            certificate_arn=certificate_arn_or_id,
            default_actions=[aws.lb.ListenerDefaultActionArgs(
                type="forward",
                target_group_arn=self.target_group.arn
            )],
            opts=pulumi.ResourceOptions(parent=self)
        )

    def _create_target_group(self):
        self.target_group = aws.lb.TargetGroup(
            f"{self._name}-tg",
            port=config.lb_backend_port_min,
            protocol="HTTP",
            vpc_id=self.vpc_id,
            target_type="ip",
            health_check=aws.lb.TargetGroupHealthCheckArgs(
                enabled=True,
                interval=config.lb_health_check_interval,
                path=config.lb_health_check_path,
                port="traffic-port",
                protocol="HTTP",
                timeout=5,
                healthy_threshold=3,
                unhealthy_threshold=3,
            ),
            opts=pulumi.ResourceOptions(parent=self)
        )
