# Implementation Plan: K8s Base Infrastructure

**Branch**: `004-k8s-base-infra` | **Date**: 2026-06-11 | **Spec**: [specs/004-k8s-base-infra/spec.md](specs/004-k8s-base-infra/spec.md)

**Input**: Feature specification from `specs/004-k8s-base-infra/spec.md`

## Summary

This feature establishes an automated, cloud-agnostic infrastructure blueprint to provision a secure, highly available Container Orchestrator and its associated Compute Node Pools. The implementation will focus on multi-zone distribution, zero-trust network perimeter, and federated identity integration.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: Pulumi, `infra` (project-local library)

**Storage**: Remote storage for infrastructure state (configured in Pulumi backend), 90-day WORM storage for security logs.

**Testing**: `pytest` (mock-based unit testing)

**Target Platform**: Cloud Orchestrator (Kubernetes)

**Project Type**: Infrastructure-as-Code

**Performance Goals**: N/A (Standard IaC expectations)

**Constraints**: Zero public exposure of compute hosts, passwordless authentication, 90-day log retention in WORM storage.

**Scale/Scope**: Multi-AZ, multi-compute-node-pool deployment.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **SOLID Engineering**: Implementation will extend `VpnComponent` patterns if necessary or introduce new base component classes following the SRP.
- [x] **Factory-Driven Provisioning**: A new `OrchestratorProviderFactory` will be introduced to handle agnostic provisioning.
- [x] **Component-Based Architecture**: All new resources will be encapsulated in `OrchestratorComponent` classes.
- [x] **Typed and Validated Configuration**: New config fields will be added to `InfrastructureConfig` with validation logic.
- [x] **Mock-First Unit Testing**: All logic will be testable via `pulumi` mocks.

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-base-infra/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/           
└── tasks.md             
```

### Source Code

```text
infra/
├── orchestrator/
│   ├── base.py          # Abstract base classes
│   ├── aws_k8s.py       # Cloud provider implementation
│   ├── azure_k8s.py
│   └── gcp_k8s.py
├── config.py            # Updated configuration
└── constants.py         # Updated constants

tests/
├── orchestrator/
│   ├── test_aws_k8s.py
│   └── test_factory.py
```

**Structure Decision**: Option 1: Single project (following existing infra structure: `infra/vpc`, `infra/lb`, `infra/vpn`). We will add `infra/orchestrator`.
