"""
🇪🇸 Implementación de AWS para el componente de Base de Datos (Amazon RDS).
Garantiza aislamiento de red, alta disponibilidad y protección de datos.

🇺🇸 AWS implementation for Database component (Amazon RDS).
Ensures network isolation, high availability, and data protection.
"""

import pulumi
import pulumi_aws as aws
from typing import List, Optional
from .base import DatabaseComponent, DatabaseOutputs
from ..config import database_config, config

class AwsDatabase(DatabaseComponent):
    """
    🇪🇸 Componente de Base de Datos para AWS.
    🇺🇸 Database component for AWS.
    """
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__('custom:aws:DatabaseComponent', name, opts)
        self._name = name
        self.subnet_group: Optional[aws.rds.SubnetGroup] = None
        self.security_group: Optional[aws.ec2.SecurityGroup] = None
        self.vpc_id: Optional[pulumi.Input[str]] = None

    def configure_network(self, vpc_id: pulumi.Input[str], subnet_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Crea un grupo de subredes RDS en las subredes aisladas proporcionadas (FR-001, FR-002).
        🇺🇸 Creates an RDS subnet group in the provided isolated subnets (FR-001, FR-002).
        """
        self.vpc_id = vpc_id
        self.subnet_group = aws.rds.SubnetGroup(
            f"{self._name}-sng",
            subnet_ids=subnet_ids,
            tags={**config.tags, "Name": f"{self._name}-sng"},
            opts=pulumi.ResourceOptions(parent=self)
        )

    def configure_security(self, authorized_source_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Configura reglas de firewall (Security Groups) para acceso restringido (FR-004, FR-005, FR-006).
        🇺🇸 Configures firewall rules (Security Groups) for restricted access (FR-004, FR-005, FR-006).
        """
        self.security_group = aws.ec2.SecurityGroup(
            f"{self._name}-sg",
            vpc_id=self.vpc_id,
            description="Perimeter firewall for Database (FR-004)",
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=database_config.port,
                    to_port=database_config.port,
                    security_groups=authorized_source_ids,
                    description="Allow DB port from authorized compute nodes (FR-005)"
                )
            ],
            egress=[], # FR-006: Deny All outbound by default (empty list)
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

    def provision(self) -> DatabaseOutputs:
        """
        🇪🇸 Provisión de instancia RDS con Multi-AZ, cifrado y protección (FR-003, FR-007, FR-008).
        🇺🇸 Provisions RDS instance with Multi-AZ, encryption, and protection (FR-003, FR-007, FR-008).
        """
        # Multi-AZ based on config (FR-003)
        # Encryption at rest with AES-256 (FR-007)
        # Deletion protection (FR-008)
        
        db_instance = aws.rds.Instance(
            f"{self._name}-db",
            engine=database_config.engine,
            engine_version=database_config.engine_version,
            instance_class=database_config.instance_class,
            allocated_storage=database_config.storage_gb,
            db_subnet_group_name=self.subnet_group.name if self.subnet_group else None,
            vpc_security_group_ids=[self.security_group.id] if self.security_group else [],
            multi_az=database_config.multi_az,
            storage_encrypted=database_config.encryption_enabled,
            deletion_protection=database_config.deletion_protection_enabled,
            skip_final_snapshot=True,
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

        return DatabaseOutputs(
            endpoint=db_instance.address,
            port=db_instance.port,
            database_name=db_instance.db_name.apply(lambda x: x or "default"),
            master_username=pulumi.Output.secret(db_instance.username)
        )
