# Research: Secure Multi-Zone Automated Compute Data Plane

## Overview
This feature requires implementing multi-zone infrastructure provisioning for compute data planes across AWS, Azure, and GCP, adhering to strict network isolation and perimeter security.

## Technical Context & Decisions

### Multi-Zone Subnet Strategy
- **Decision**: Leverage standardized provider-specific subnet tagging and availability zone mapping to ensure uniform distribution.
- **Rationale**: Ensures resilience against single-zone failures as required by P1 story.
- **Alternatives Considered**: Manual subnet ID overrides (too fragile/coupled).

### Perimeter Security
- **Decision**: Utilize native cloud security group/firewall rules with "deny-by-default" and explicit allow-rules only for essential traffic.
- **Rationale**: Aligns with the P3 story and strict perimeter enforcement requirements.
- **Alternatives Considered**: Host-based iptables (too difficult to maintain at scale/orchestration level).

### Identity Governance
- **Decision**: Assign distinct IAM roles/service accounts per orchestrator component, limited to essential cluster management operations.
- **Rationale**: Satisfies the P4 story (minimum privilege).
- **Alternatives Considered**: Generic "all-purpose" roles (violates principle of least privilege).

### Idempotency and Scaling
- **Decision**: The infrastructure automation will target *structural* configuration (network, IAM, security groups) while leaving *runtime* host-count management to an external auto-scaling engine.
- **Rationale**: Ensures the infrastructure blueprint doesn't conflict with active scaling (P2 story).
- **Alternatives Considered**: Direct management of host-count within Pulumi (creates race conditions).

## Open Questions/Assumptions (Resolved)
- **Resolved**: "NEEDS CLARIFICATION: auth method" -> *Assumption*: Use standard cloud-provider IAM/ServiceAccount native mechanisms (e.g., OIDC for K8s, IAM roles for VMs).
- **Resolved**: "NEEDS CLARIFICATION: retention period" -> *Assumption*: Use standard platform logging/metric retention defaults for the compute tier.
