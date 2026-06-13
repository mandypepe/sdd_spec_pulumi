# Research: Workload Identity Federation (K8s)

## Overview
This research document addresses the requirements for HU-009, establishing secure identity federation for Kubernetes workloads across AWS, Azure, and GCP.

## Decision: Identity Component Isolation
**Rationale**: Decouple identity federation from K8s orchestrators to adhere to SOLID principles (SRP). `IdentityComponent` will manage OIDC trust relationships independently.
**Alternatives Considered**:
- Integrate into `OrchestratorComponent` (Rejected: Bloats orchestrator complexity).

## Decision: OIDC Identity Mapping
| Feature | AWS (IRSA) | Azure (Workload Identity) | GCP (Workload Identity) |
|---------|-----|-------|-----|
| OIDC Provider | AWS IAM OIDC Provider | Azure AD Federated Identity | GCP Workload Identity Pool |
| Trust Source | K8s Service Account Token | K8s Service Account Token | K8s Service Account Token |
| Association | IAM Role | User-Assigned Managed Identity | GCP Service Account |

## Decision: Idempotency & Lifecycle
**Rationale**: Ensure deployments are repeatable and protected.
**Implementation**: Use standard Pulumi `ResourceOptions(protect=True)` and ensure OIDC provider creation checks for existence before creation (where applicable).

## Decision: Performance & Scale
**Rationale**: Identity federation operates at the OIDC control plane level. Impact on application latency is non-existent as tokens are issued out-of-band and refreshed locally by the K8s pod SDK.
