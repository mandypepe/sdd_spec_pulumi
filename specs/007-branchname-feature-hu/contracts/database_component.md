# Contract: DatabaseComponent

## Overview
The `DatabaseComponent` provides a unified interface for provisioning managed relational databases across AWS, Azure, and GCP. It ensures that security, high availability, and isolation standards are enforced globally.

## Class Definition

```python
class DatabaseComponent(pulumi.ComponentResource):
    """
    Abstract base class for managed multi-cloud databases.
    """
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__('pkg:index:DatabaseComponent', name, None, opts)

    @abstractmethod
    def configure_network(self, vpc_id: str, subnet_ids: List[str]):
        """
        Allocates the database to private subnets.
        Enforces no public routes.
        """
        pass

    @abstractmethod
    def configure_security(self, authorized_source_ids: List[str]):
        """
        Sets up the perimeter firewall (Security Groups/Firewall Rules).
        Restricts ingress to authorized sources and egress to none.
        """
        pass

    @abstractmethod
    def provision(self) -> DatabaseOutputs:
        """
        Initializes the managed database cluster.
        Enforces encryption-at-rest (AES-256) and deletion protection.
        """
        pass
```

## Expected Outputs

All implementations must return a `DatabaseOutputs` object with the following secret-wrapped fields:
- `endpoint`: The private FQDN of the database.
- `master_username`: The administrative username.
- `master_password_ref`: A reference to the generated password in the cloud provider's secret store.
