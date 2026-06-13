# Data Model: Automated Secrets Vault

## Entities

### CryptographicVaultInstance
- `identifier`: str (Unique ID)
- `availability_zones`: list[str] (Zones for multi-zone deployment)
- `non_destruction_flag`: bool (Prevent deletion)
- `soft_retention_days`: int (Default 30)

### MasterEncryptionKey
- `key_identifier`: str
- `rotation_interval_days`: int (Default 90)

### PerimeterFirewallRule
- `allowed_subnets`: list[str] (e.g., `10.0.10.0/23`, `10.0.12.0/23`)
- `target_port`: int (443)

### FederatedWorkloadIdentity
- `namespace`: str
- `service_account`: str
- `access_role`: str

### StructuralSecretBlueprint
- `secret_path`: str
- `database_host_placeholder`: str
- `ephemeral_password_ttl_minutes`: int (Default 60)
