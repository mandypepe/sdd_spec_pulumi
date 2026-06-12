# Contract: Orchestrator Component Interface

This file defines the public interface that any provider-specific Orchestrator implementation MUST satisfy.

## Interface: `OrchestratorComponent` (Abstract Base Class)

Any new provider (AWS, Azure, GCP) must implement the following methods to ensure factory compatibility:

### Constructor
`__init__(self, name: str, config: OrchestratorConfig, opts: pulumi.ResourceOptions)`

### Required Methods
- `_create_network_boundary(self) -> NetworkBoundary`
    - MUST configure firewall/security group rules based on `config`.
    - MUST implement "deny-by-default" logic.

- `_create_host_identity(self) -> HostIdentity`
    - MUST create/attach a least-privilege identity to compute hosts.

- `_provision_compute_tier(self) -> None`
    - MUST distribute nodes across `availability_zones` (min 2).
    - MUST ignore variance in host count to support runtime auto-scaling.
