<!--
Sync Impact Report
- Version change: 0.0.0 -> 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] -> SOLID Engineering
    - [PRINCIPLE_2_NAME] -> Factory-Driven Provisioning
    - [PRINCIPLE_3_NAME] -> Component-Based Architecture
    - [PRINCIPLE_4_NAME] -> Typed and Validated Configuration
    - [PRINCIPLE_5_NAME] -> Mock-First Unit Testing
- Added sections: Infrastructure Standards, Development Workflow
- Removed sections: None
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated)
    - .specify/templates/spec-template.md (✅ updated)
    - .specify/templates/tasks-template.md (✅ aligned)
- Follow-up TODOs: None
-->

# Pulumi Multi-Cloud VPN Infrastructure Constitution

## Core Principles

### I. SOLID Engineering
Adhere to SRP, OCP, LSP, ISP, and DIP. Each module must have a single responsibility. New cloud providers must be added by extending the base classes without modifying the core factory or existing logic. Use abstract base classes (`VpnComponent`) and dependency injection via Pulumi options.

### II. Factory-Driven Provisioning
Use the `VpnProviderFactory` pattern to instantiate resources dynamically based on the selected provider. This ensures the main entry point (`main.py`) remains agnostic of specific cloud provider implementation details, facilitating multi-cloud support and testability.

### III. Component-Based Architecture
All cloud resources must be grouped into logical `ComponentResource` units (e.g., `AwsVpnComponent`). Child resources must explicitly set `pulumi.ResourceOptions(parent=self)` to maintain a strict dependency hierarchy and ensure a clean, organized infrastructure graph.

### IV. Typed and Validated Configuration
Centralize all infrastructure parameters in the `InfrastructureConfig` class. All configuration must be accessed via the `config` singleton. Inputs must be validated at program start to ensure fail-fast behavior. Avoid "magic strings" or hardcoded values outside of `constants.py`.

### V. Mock-First Unit Testing
Every infrastructure component must be verifiable using Pulumi mocks. Unit tests in `tests/` must validate resource properties and logical branchings. A feature is not considered complete until its logic passes the mock-based test suite, ensuring reliability without cloud credentials.

## Infrastructure Standards

- **Resource Naming**: Follow the `{name}-{resource_type}` convention (e.g., `vpn-vpc`) to ensure consistent naming across providers.
- **Resource Tagging**: All resources must inherit standard tags from `config.tags` (e.g., `Project`, `Environment`, `Managed-By`).
- **Network Consistency**: Use standard CIDR ranges and network definitions from `constants.py` to prevent overlap in multi-cloud deployments.
- **Bilingual Documentation**: All docstrings, comments, and major documentation must be provided in both Spanish (🇪🇸) and English (🇺🇸).

## Development Workflow

- **Specify Process**: Follow the `Spec -> Plan -> Implement` cycle for all significant features or provider additions.
- **Verification**: Run `pytest` with `PYTHONPATH="."` before every commit.
- **Extension Guide**: To add a new provider, implement the `VpnComponent` interface, register it in the factory, and add corresponding tests.

## Governance

This constitution is the foundational document for architectural decisions in the Pulumi Multi-Cloud VPN Infrastructure project. Any deviation from these principles must be documented and justified in the implementation plan. Amendments require a version bump and ratification.

**Version**: 1.0.0 | **Ratified**: 2026-06-09 | **Last Amended**: 2026-06-09
