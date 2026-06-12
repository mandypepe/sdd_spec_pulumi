# Contract: LbComponent Interface

The `LbComponent` is a Pulumi `ComponentResource` that provides a unified interface for deploying public-facing Layer 7 load balancers across multiple cloud providers.

## Constructor Contract

All provider-specific implementations (e.g., `AwsLbComponent`) must adhere to this initialization contract.

```python
class LbComponent(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        vpc_id: pulumi.Input[str],
        public_subnet_ids: pulumi.Input[list[str]],
        certificate_arn_or_id: str,
        opts: Optional[pulumi.ResourceOptions] = None,
        config: Optional[LbConfig] = None
    ):
        """
        Initializes the Load Balancer component.
        
        Args:
            name: Logical name of the component.
            vpc_id: The ID of the VPC where the LB will be deployed.
            public_subnet_ids: List of at least two public subnet IDs in different AZs.
            certificate_arn_or_id: Reference (ARN, ID, or Name) to a pre-existing SSL certificate.
            opts: Pulumi resource options.
            config: Optional override configuration for port ranges, health checks, etc.
        """
        ...
```

## Configuration Schema (`LbConfig`)

```python
class LbConfig:
    backend_port_min: int = 30000
    backend_port_max: int = 32767
    health_check_path: str = "/healthz"
    health_check_interval: int = 15
    enable_deletion_protection: bool = True
    ssl_policy: str = "TLS1.3-Strict" # Provider-mapped to specific policy names
```

## Exposed Outputs

| Output | Type | Description |
|--------|------|-------------|
| `dns_name` | `Output[str]` | The public DNS name of the load balancer. |
| `lb_arn_or_id` | `Output[str]` | The provider-specific identifier for the load balancer. |
| `security_group_id` | `Output[str]` | The ID of the perimeter security group/filter created. |

## Provider Mappings

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| TLS 1.3 Policy | `ELBSecurityPolicy-TLS13-1-2-Res-2021-06` | `CustomV2` (Min TLS 1.3) | `MODERN` Profile (Min TLS 1.2) |
| Deletion Protection | `enable_deletion_protection=True` | `ManagementLock (CanNotDelete)` | `delete_protection=True` |
| Health Check | `TargetGroup.health_check.interval` | `ApplicationGatewayProbe.interval` | `HealthCheck.check_interval_sec` |
