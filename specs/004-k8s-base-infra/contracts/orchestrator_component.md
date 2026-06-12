# Contract: Orchestrator Component Interface

This contract defines the interface that all provider-specific orchestrator components MUST implement to be integrated into the infrastructure framework.

## Interface: `OrchestratorComponent`

```python
class OrchestratorComponent(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        config: OrchestratorConfig,
        opts: pulumi.ResourceOptions = None
    ):
        ...
```

### Required Methods
- **Provision**: Must initialize the orchestrator cluster control plane and compute node pools across the specified availability zones.
- **ConfigureSecurity**: Must configure firewall rules to block incoming administrative traffic and route outbound traffic via secure translation gateways.
- **ConfigureIdentity**: Must integrate with the cloud provider's OIDC or identity service to enable token-based authentication.

### Input Constraints
- `config`: Must contain validated `az_list`, `min_size`, `max_size`, and network configuration.
- Public IPs MUST be disabled in all resource configurations.
