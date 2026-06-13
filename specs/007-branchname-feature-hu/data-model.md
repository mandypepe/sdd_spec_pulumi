# Data Model: Managed Database Infrastructure

## Entities

### DatabaseComponent (Abstract)
The base class for all cloud-specific database implementations.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Logical name of the database component |
| engine | string | Database engine (e.g., 'postgres', 'mysql') |
| version | string | Engine version |
| instance_class | string | Compute capacity of the instances |
| storage_gb | int | Allocated storage in GB |
| multi_az | bool | Whether to enable high availability |
| encryption | bool | Whether to enable AES-256 encryption |
| deletion_protection | bool | Whether to enable lifecycle protection |

### DatabaseOutputs (Secure Metadata)
Metadata exported after successful provisioning.

| Field | Type | Description |
|-------|------|-------------|
| endpoint | Output[string] | Connection endpoint (Secret) |
| port | Output[int] | Service port |
| database_name | Output[string] | Primary database name |
| master_username | Output[string] | Admin username (Secret) |

## State Transitions

1. **Pending**: Resources defined but not yet requested from the provider.
2. **Provisioning**: Pulumi is creating the subnets and database cluster.
3. **Active**: Database is available and accepting connections from authorized compute nodes.
4. **Protected**: Deletion protection is active, preventing accidental removal.
5. **Terminating**: (Blocked by protection unless explicitly overridden).
