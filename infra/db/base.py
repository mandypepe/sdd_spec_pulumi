"""
🇪🇸 Clase base abstracta para componentes de Base de Datos (Abstract Base Class & Component Pattern).
Define el contrato común para todas las implementaciones de bases de datos administradas multi-cloud.

🇺🇸 Abstract base class for Database components (Abstract Base Class & Component Pattern).
Defines common interface for all multi-cloud managed database implementations.
"""

from abc import ABC, abstractmethod
import pulumi
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class DatabaseOutputs:
    """
    🇪🇸 Metadatos exportados después de un aprovisionamiento exitoso.
    Todos los campos sensibles se envuelven como secretos de Pulumi.

    🇺🇸 Metadata exported after successful provisioning.
    All sensitive fields are wrapped as Pulumi secrets.
    """
    endpoint: pulumi.Output[str]
    port: pulumi.Output[int]
    database_name: pulumi.Output[str]
    master_username: pulumi.Output[str]
    master_password_ref: Optional[pulumi.Output[str]] = None


class DatabaseComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Clase base abstracta para bases de datos administradas multi-cloud.
    Sigue rigurosamente la arquitectura de componentes papá-hijo en Pulumi.

    🇺🇸 Abstract base class for multi-cloud managed databases.
    Strictly adheres to Pulumi's parent-child component resource architecture.
    """

    def __init__(
        self,
        resource_type: str,
        name: str,
        opts: Optional[pulumi.ResourceOptions] = None
    ):
        """
        🇪🇸 Inicializa el componente de Base de Datos base.

        🇺🇸 Initializes the base Database component.

        Args:
            resource_type: 🇪🇸 Tipo de recurso Pulumi / 🇺🇸 Pulumi resource type
            name: 🇪🇸 Nombre lógico del componente / 🇺🇸 Logical component name
            opts: 🇪🇸 Opciones de recursos Pulumi / 🇺🇸 Pulumi ResourceOptions
        """
        super().__init__(resource_type, name, opts=opts)

    @abstractmethod
    def configure_network(self, vpc_id: pulumi.Input[str], subnet_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Asigna la base de datos a subredes privadas aisladas.
        Garantiza que no existan rutas públicas (FR-001, FR-002).

        🇺🇸 Allocates the database to isolated private subnets.
        Ensures no public routes exist (FR-001, FR-002).
        """
        pass

    @abstractmethod
    def configure_security(self, authorized_source_ids: pulumi.Input[List[str]]):
        """
        🇪🇸 Configura el firewall perimetral (Grupos de Seguridad/Reglas de Firewall).
        Restringe el ingreso a fuentes autorizadas y el egreso a ninguna (FR-004, FR-005, FR-006).

        🇺🇸 Sets up the perimeter firewall (Security Groups/Firewall Rules).
        Restricts ingress to authorized sources and egress to none (FR-004, FR-005, FR-006).
        """
        pass

    @abstractmethod
    def provision(self) -> DatabaseOutputs:
        """
        🇪🇸 Inicializa el clúster de base de datos administrada.
        Impone cifrado en reposo (AES-256) y protección contra eliminación (FR-003, FR-007, FR-008).

        🇺🇸 Initializes the managed database cluster.
        Enforces encryption-at-rest (AES-256) and deletion protection (FR-003, FR-007, FR-008).
        """
        pass
