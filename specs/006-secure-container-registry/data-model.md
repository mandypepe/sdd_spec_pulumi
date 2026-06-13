# Data Model: Secure Container Registry

## Entities

### SecureRegistry
Represents the central isolated storage asset containing the repositories, core operational configurations, and encryption keys.

| Field | Type | Description |
|-------|------|-------------|
| name | String | Identifier for the registry component. |
| region | String | Target cloud region. |
| encryption_key_id | String | ARN/ID of enterprise-managed KMS key. |
| tag_immutability | Boolean | Enabled by default to prevent overwrites. |
| encryption_at_rest | Boolean | Enabled by default using enterprise key. |

### AccessControlPolicy
Defines the structural mapping between system identities and permitted interactions.

| Field | Type | Description |
|-------|------|-------------|
| registry_id | String | Reference to SecureRegistry. |
| reader_identities | List[String] | Identities allowed to Read Only (e.g., K8s nodes). |
| writer_identities | List[String] | Identities allowed to Read/Write (e.g., CI pipelines). |

### LifecycleRule
Automated scheduling instruction for expiring assets.

| Field | Type | Description |
|-------|------|-------------|
| registry_id | String | Reference to SecureRegistry. |
| untagged_retention_days | Integer | Days before untagged images are deleted. |
| max_untagged_count | Integer | Max number of untagged images to retain. |

### SoftwareAsset
The versioned container package.

| Field | Type | Description |
|-------|------|-------------|
| registry_id | String | Reference to SecureRegistry. |
| repository_name | String | Name of the repository. |
| image_tag | String | Immutable version tag. |
| encryption_state | String | Current encryption status. |
| scan_result | String | Latest vulnerability scan summary. |
