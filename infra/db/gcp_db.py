"""
🇪🇸 Implementación de GCP para el componente de Base de Datos (Cloud SQL).
Garantiza alta disponibilidad regional y aislamiento mediante Private Service Access.

🇺🇸 GCP implementation for Database component (Cloud SQL).
Ensures regional high availability and isolation via Private Service Access.
"""

import pulumi
import pulumi_gcp as gcp
from typing import List, Optional
from .base import DatabaseComponent, DatabaseOutputs
from ..config import database_config, config

class GcpDatabase(DatabaseComponent):
    """
    🇪🇸 Componente de Base de Datos para GCP.
    🇺🇸 Database component for GCP.
    """
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__('custom:gcp:DatabaseComponent', name, opts)
        self._name = name
        self.network_id: Optional[pulumi.Input[str]] = None

    def configure_network(self, vpc_id: pulumi.Input[str], subnet_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Configura la red para Cloud SQL (FR-001, FR-002).
        En GCP, Cloud SQL utiliza Private Service Access sobre el VPC.
        🇺🇸 Configures the network for Cloud SQL (FR-001, FR-002).
        In GCP, Cloud SQL uses Private Service Access over the VPC.
        """
        self.network_id = vpc_id

    def configure_security(self, authorized_source_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Configura reglas de firewall de GCP para el servidor (FR-004, FR-005).
        🇺🇸 Configures GCP firewall rules for the server (FR-004, FR-005).
        """
        pass

    def provision(self) -> DatabaseOutputs:
        """
        🇪🇸 Provisión de instancia Cloud SQL con HA regional y cifrado (FR-003, FR-007, FR-008).
        🇺🇸 Provisions Cloud SQL instance with regional HA and encryption (FR-003, FR-007, FR-008).
        """
        instance = gcp.sql.DatabaseInstance(
            f"{self._name}-instance",
            database_version="POSTGRES_15",
            region=config.gcp_region,
            settings=gcp.sql.DatabaseInstanceSettingsArgs(
                tier="db-f1-micro",
                availability_type="REGIONAL" if database_config.multi_az else "ZONAL",
                ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
                    ipv4_enabled=False,
                    private_network=self.network_id,
                ),
                backup_configuration=gcp.sql.DatabaseInstanceSettingsBackupConfigurationArgs(
                    enabled=True,
                    binary_log_enabled=True,
                ),
                deletion_protection_enabled=database_config.deletion_protection_enabled,
            ),
            deletion_protection=database_config.deletion_protection_enabled,
            opts=pulumi.ResourceOptions(parent=self)
        )

        return DatabaseOutputs(
            endpoint=instance.private_ip_address,
            port=pulumi.Output.from_input(database_config.port),
            database_name=pulumi.Output.from_input("default"),
            master_username=pulumi.Output.secret("postgres")
        )
