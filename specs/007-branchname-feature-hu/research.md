# Research: Provisioning of a Managed Database in an Isolated Layer

## Decision: Technology Stack and Implementation Patterns

- **AWS**: Use `aws.rds.Instance` or `aws.rds.Cluster` (Aurora) with `multi_az=True`, `storage_encrypted=True`, `kms_key_id` for AES-256, and `deletion_protection=True`.
- **Azure**: Use `azure.postgresql.FlexibleServer` or `azure.sql.ManagedInstance` with High Availability (Zone-redundant), transparent data encryption (TDE), and resource locks.
- **GCP**: Use `gcp.sql.DatabaseInstance` with `settings.availability_type="REGIONAL"`, `settings.backup_configuration.enabled=True`, and `deletion_protection=True`.
- **Network**: Private subnets in a dedicated VPC/VNET/VPC Network. Routing tables will have no route to `0.0.0.0/0`.
- **Secure Outputs**: Use `pulumi.Output.secret()` to ensure sensitive connection data is masked in logs and state.

## Rationale

- **High Availability**: The spec requires < 60s failover. Multi-AZ/Regional availability types are the standard managed solutions for this.
- **Security**: AES-256 is natively supported by KMS/TDE on all providers. Isolated subnets prevent public access.
- **Protection**: Deletion protection at the resource level prevents accidental `pulumi destroy` from removing databases.

## Alternatives Considered

- **Self-managed DBs on VMs**: Rejected because managed services provide better SLA, automatic patching, and native HA/encryption integration with less operational overhead.
- **Public subnets with IP whitelisting**: Rejected due to US1 (Complete Network Segregation).
