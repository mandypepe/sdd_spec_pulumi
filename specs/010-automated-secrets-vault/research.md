# Research: Automated Secrets Vault

## Unknowns & Decisions

- **Decision: Vault Provider Abstraction**
    - **Rationale**: Project must support multi-cloud providers (AWS/Azure/GCP).
    - **Alternatives considered**: Vendor-specific vault services (rejected due to cloud-agnostic principle).
- **Decision: OIDC Integration Pattern**
    - **Rationale**: Workload identity federation using OIDC tokens is standard and secure.
    - **Alternatives considered**: Static credential management (rejected due to hardcoded key risk).
- **Decision: Network Isolation**
    - **Rationale**: Vault interface restricted to private subnet ranges via firewall rules.
    - **Alternatives considered**: Public-facing endpoint with IP-based access control (rejected due to security risk).
