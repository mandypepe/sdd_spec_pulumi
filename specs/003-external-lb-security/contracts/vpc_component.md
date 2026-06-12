# Contract: PublicTrafficManager Interface

This contract defines the interface for the `PublicTrafficManager` component, which must be implemented for each supported cloud provider (AWS, Azure, GCP).

## Interface Signature

```python
class PublicTrafficManager(pulumi.ComponentResource):
    def __init__(self, name: str, opts: PublicTrafficManagerArgs, ...):
        ...
```

## Argument Schema (PublicTrafficManagerArgs)

- `subnets`: List[string] (required, must be ["10.0.1.0/24", "10.0.2.0/24"])
- `certificate_arn`: string (required, pre-existing static reference)
- `health_check_path`: string (optional, default: "/healthz")
- `health_check_interval`: integer (optional, default: 15)
- `protect`: boolean (optional, default: True)
