# Quickstart: Automated Secrets Vault Validation

## Prerequisites
- Pulumi CLI installed.
- Access to multi-cloud credentials (for mock testing, not needed).
- Infrastructure project initialized.

## Setup
1. Configure `InfrastructureConfig` with vault parameters.
2. Register `VaultProviderFactory` in `infra/factory.py` or equivalent.

## Runnable Scenarios
- `pytest tests/test_vault_factory.py` (Validate factory instantiation)
- `pytest tests/test_vault_component.py` (Validate Pulumi component hierarchy and resource tagging)
- `pulumi up` (Dry-run deployment with mock providers)
