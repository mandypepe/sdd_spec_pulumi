# Registry Component Interface Contract

This contract defines the public interface that all cloud-provider-specific `RegistryComponent` implementations MUST adhere to.

## Interface: `RegistryComponent` (Abstract)

### Properties
- `registry_id`: String (read-only)
- `repository_url`: String (read-only)

### Methods
- `__init__(self, name, region, encryption_key_id, ...)`: Constructor
- `_provision_registry(self)`: Provisions the core registry.
- `_enable_immutability(self)`: Configures tag immutability.
- `_enable_vulnerability_scanning(self)`: Configures automated scanning.
- `_set_lifecycle_policy(self, rules)`: Applies retention policies.
- `_grant_access(self, identity, role)`: Maps identities to permissions.

## Validation
All implementations must be tested using the mock framework defined in `tests/registry/conftest.py`.
