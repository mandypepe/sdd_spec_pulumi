# Contract: VpcComponent Interface

## Constructor

```python
def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
    """
    Initializes a new three-tier VPC topology.
    
    Args:
        name: The unique name of the resource.
        opts: Optional Pulumi resource options.
    """
```

## Input Configuration (via InfrastructureConfig)

The component reads the following from the `config` singleton:

| Key | Type | Description |
|-----|------|-------------|
| `vpc_cidr` | `str` | The master CIDR block (default: `10.0.0.0/16`). |
| `availability_zones` | `list[str]` | The two target zones. |
| `tags` | `dict` | Standard metadata tags. |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| `vpc_id` | `Output[str]` | The ID of the primary VPC container. |
| `public_subnets` | `Output[list[str]]` | IDs of the public subnets. |
| `private_subnets` | `Output[list[str]]` | IDs of the private subnets. |
| `isolated_subnets` | `Output[list[str]]` | IDs of the isolated subnets. |
| `nat_gateways` | `Output[list[str]]` | IDs of the zone-pinned NAT gateways. |
