"""
🇪🇸 Implementación de Azure para el componente de Base de Datos (Azure PostgreSQL Flexible Server).
Enfoque en alta disponibilidad zonal y aislamiento por subred delegada.

🇺🇸 Azure implementation for Database component (Azure PostgreSQL Flexible Server).
Focus on zonal high availability and isolation via delegated subnet.
"""

import pulumi
import pulumi_azure_native as azure_native
from typing import List, Optional
from .base import DatabaseComponent, DatabaseOutputs
from ..config import database_config, config

class AzureDatabase(DatabaseComponent):
    """
    🇪🇸 Componente de Base de Datos para Azure.
    🇺🇸 Database component for Azure.
    """
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__('custom:azure:DatabaseComponent', name, opts)
        self._name = name
        self.vnet_id: Optional[pulumi.Input[str]] = None
        self.subnet_id: Optional[pulumi.Input[str]] = None

    def configure_network(self, vpc_id: pulumi.Input[str], subnet_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Almacena referencias de red para Azure (FR-001, FR-002).
        En Azure, los servidores flexibles requieren una subred delegada.
        🇺🇸 Stores network references for Azure (FR-001, FR-002).
        In Azure, flexible servers require a delegated subnet.
        """
        self.vnet_id = vpc_id
        # Assuming the first subnet provided is the one to use/delegate
        self.subnet_id = pulumi.Output.from_input(subnet_ids).apply(lambda ids: ids[0] if ids else None)

    def configure_security(self, authorized_source_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Configura reglas de firewall de Azure para el servidor (FR-004, FR-005).
        🇺🇸 Configures Azure firewall rules for the server (FR-004, FR-005).
        """
        # Azure Flexible Server uses Firewall rules or VNET integration.
        # Implementation details deferred to provision or separate resources.
        pass

    def provision(self) -> DatabaseOutputs:
        """
        🇪🇸 Provisión de Flexible Server con HA zonal y cifrado (FR-003, FR-007, FR-008).
        🇺🇸 Provisions Flexible Server with zonal HA and encryption (FR-003, FR-007, FR-008).
        """
        resource_group = azure_native.resources.ResourceGroup(
            f"{self._name}-rg",
            location=config.azure_location,
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

        server = azure_native.dbforpostgresql.Server(
            f"{self._name}-server",
            resource_group_name=resource_group.name,
            location=resource_group.location,
            sku=azure_native.dbforpostgresql.SkuArgs(
                name="Standard_D2s_v3",
                tier=azure_native.dbforpostgresql.SkuTier.GENERAL_PURPOSE,
            ),
            storage=azure_native.dbforpostgresql.StorageArgs(
                storage_size_gb=database_config.storage_gb,
            ),
            network=azure_native.dbforpostgresql.NetworkArgs(
                delegated_subnet_resource_id=self.subnet_id,
            ),
            high_availability=azure_native.dbforpostgresql.HighAvailabilityArgs(
                mode=azure_native.dbforpostgresql.HighAvailabilityMode.ZONE_REDUNDANT if database_config.multi_az else azure_native.dbforpostgresql.HighAvailabilityMode.DISABLED,
            ),
            data_encryption=azure_native.dbforpostgresql.DataEncryptionArgs(
                type=azure_native.dbforpostgresql.ArmServerKeyType.SYSTEM_MANAGED,
            ),
            version=database_config.engine_version,
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

        return DatabaseOutputs(
            endpoint=server.fully_qualified_domain_name,
            port=pulumi.Output.from_input(database_config.port),
            database_name=pulumi.Output.from_input("default"),
            master_username=pulumi.Output.secret(server.administrator_login)
        )
