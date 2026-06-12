# Research: K8s Base Infrastructure

**Goal**: Resolve uncertainties in the implementation of the K8s base infrastructure and document best practices.

## Uncertainties & Research

### 1. Federated Identity Mechanisms
- **Decision**: Implement OIDC-based federation.
- **Rationale**: Industry standard for passwordless, short-lived token authentication in cloud environments, compatible with Kubernetes (ServiceAccount token volume projection).
- **Alternatives considered**: Static long-lived tokens (rejected - insecure), manual key rotation (rejected - high operational burden).

### 2. Immutable WORM Storage for Security Logs
- **Decision**: Leverage cloud provider native WORM capabilities (e.g., S3 Object Lock in compliance mode, Azure Immutable Blob Storage with policy).
- **Rationale**: Ensures compliance with the requirement without needing custom software solutions.
- **Alternatives considered**: Third-party log management services (rejected - increased dependency, cost), standard object storage with manual deletion restriction (rejected - less secure/compliant).

### 3. Baseline Tracking Override Pattern
- **Decision**: Utilize Pulumi's `ignore_changes` resource option for autoscaling-managed attributes in compute node pools.
- **Rationale**: Idiomatic Pulumi approach to prevent drift/reversion during runtime scaling adjustments while maintaining base infra definitions in code.
- **Alternatives considered**: Separate automation tool for scaling (rejected - introduces external dependencies), hardcoded fleet dimensions (rejected - prevents autoscaling).

## Best Practices

- **Security**: Strict enforcement of private-only subnets for control plane and compute nodes. No public IPs permitted.
- **Availability**: Mandatory distribution across at least two availability zones.
- **Identity**: Usage of minimal-privilege ServiceAccount roles based on actual workload needs (registry pull and telemetry).
- **Isolation**: Blueprint definitions for infrastructure completely separate from application charts.
