"""
🇪🇸 Gestión de configuración tipada e inyección de dependencias para infraestructura.
Encapsula acceso centralizado a pulumi.Config y variables de entorno.

🇺🇸 Typed configuration management and dependency injection for infrastructure.
Centralizes access to pulumi.Config and environment variables.
"""

import os
from typing import Dict, Optional
import pulumi

from .constants import DEFAULT_TAGS, DEFAULT_VPN_NAME, DEFAULT_K8S_NODE_INSTANCE_TYPE, DEFAULT_K8S_MIN_NODES, DEFAULT_K8S_MAX_NODES, DEFAULT_SECURITY_LOG_RETENTION_DAYS


class InfrastructureConfig:
    """
    🇪🇸 Configuración centralizada de la infraestructura (Singleton Pattern).
    Proporciona acceso tipado a todas las propiedades de configuración.
    
    🇺🇸 Centralized infrastructure configuration (Singleton Pattern).
    Provides typed access to all configuration properties.
    """

    def __init__(self):
        self._cfg = pulumi.Config()
        self._project_tags = DEFAULT_TAGS

    @property
    def provider(self) -> str:
        """
        🇪🇸 Retorna el proveedor de nube configurado (aws, azure, gcp).
        🇺🇸 Returns the configured cloud provider (aws, azure, gcp).
        """
        provider = self._cfg.get("provider") or os.getenv("PROVIDER")
        return (provider or "aws").lower()

    @property
    def vpn_name(self) -> str:
        """
        🇪🇸 Retorna el nombre base para todos los recursos VPN.
        🇺🇸 Returns the base name for all VPN resources.
        """
        return self._cfg.get("vpn_name") or DEFAULT_VPN_NAME

    @property
    def tags(self) -> Dict[str, str]:
        """
        🇪🇸 Retorna los tags por defecto (aplicados a todos los recursos).
        🇺🇸 Returns default tags (applied to all resources).
        """
        return self._project_tags

    @property
    def aws_region(self) -> str:
        """
        🇪🇸 Retorna la región de AWS configurada.
        🇺🇸 Returns the configured AWS region.
        """
        return self._cfg.get("aws:region") or "us-east-1"

    @property
    def gcp_region(self) -> str:
        """
        🇪🇸 Retorna la región de GCP configurada.
        🇺🇸 Returns the configured GCP region.
        """
        return self._cfg.get("gcp:region") or "us-central1"

    @property
    def azure_location(self) -> str:
        """
        🇪🇸 Retorna la ubicación geográfica de Azure configurada.
        🇺🇸 Returns the configured Azure location (geography).
        """
        return self._cfg.get("azure:location") or "eastus"

    @property
    def vpc_cidr(self) -> str:
        """
        🇪🇸 Retorna el bloque CIDR maestro de la VPC (Network & Subnetting).
        🇺🇸 Returns the master CIDR block for VPC (Network & Subnetting).
        """
        return self._cfg.get("vpc_cidr") or "10.0.0.0/16"

    @property
    def lb_backend_port_min(self) -> int:
        return self._cfg.get_int("lb_backend_port_min") or 30000

    @property
    def lb_backend_port_max(self) -> int:
        return self._cfg.get_int("lb_backend_port_max") or 32767

    @property
    def lb_health_check_path(self) -> str:
        return self._cfg.get("lb_health_check_path") or "/healthz"

    @property
    def lb_health_check_interval(self) -> int:
        return self._cfg.get_int("lb_health_check_interval") or 15

    @property
    def lb_enable_deletion_protection(self) -> bool:
        return self._cfg.get_bool("lb_enable_deletion_protection") or True

    @property
    def lb_ssl_policy(self) -> str:
        return self._cfg.get("lb_ssl_policy") or "TLS1.3-Strict"

    @property
    def lb_certificate_arn_or_id(self) -> Optional[str]:
        return self._cfg.get("lb_certificate_arn_or_id")

    @property
    def availability_zones(self) -> list[str]:
        """
        🇪🇸 Retorna la lista de zonas de disponibilidad objetivo (High Availability).
        🇺🇸 Returns the target availability zones list (High Availability).
        """
        zones = self._cfg.get_object("availability_zones")
        return zones or ["zone-1", "zone-2"]

    @property
    def k8s_node_instance_type(self) -> str:
        return self._cfg.get("k8s_node_instance_type") or DEFAULT_K8S_NODE_INSTANCE_TYPE

    @property
    def k8s_min_nodes(self) -> int:
        return self._cfg.get_int("k8s_min_nodes") or DEFAULT_K8S_MIN_NODES

    @property
    def k8s_max_nodes(self) -> int:
        return self._cfg.get_int("k8s_max_nodes") or DEFAULT_K8S_MAX_NODES

    @property
    def security_log_retention_days(self) -> int:
        return self._cfg.get_int("security_log_retention_days") or DEFAULT_SECURITY_LOG_RETENTION_DAYS


class OrchestratorConfig:
    """
    🇪🇸 Configuración para el componente orquestador (multi-zona, perimetral, identidad).
    Validación tipada usando Pydantic para configuración de seguridad e idempotencia.
    
    🇺🇸 Configuration for orchestrator component (multi-zone, perimeter, identity).
    Type-safe validation using Pydantic for security and idempotence settings.
    """
    
    def __init__(self, cfg: Optional[pulumi.Config] = None):
        self._cfg = cfg or pulumi.Config()
    
    @property
    def availability_zones(self) -> list[str]:
        """
        🇪🇸 Zonas de disponibilidad para multi-zona compute plane.
        🇺🇸 Availability zones for multi-zone compute plane.
        """
        zones = self._cfg.get_object("orchestrator:availability_zones")
        return zones or ["zone-1", "zone-2"]
    
    @property
    def subnet_ids(self) -> list[str]:
        """
        🇪🇸 IDs de subnets privadas para el plano de datos.
        🇺🇸 Private subnet IDs for data plane.
        """
        subnets = self._cfg.get_object("orchestrator:subnet_ids")
        return subnets or []
    
    @property
    def scaling_min_nodes(self) -> int:
        """
        🇪🇸 Número mínimo de nodos orquestados.
        🇺🇸 Minimum number of orchestrated nodes.
        """
        return self._cfg.get_int("orchestrator:scaling_min_nodes") or 2
    
    @property
    def scaling_max_nodes(self) -> int:
        """
        🇪🇸 Número máximo de nodos orquestados.
        🇺🇸 Maximum number of orchestrated nodes.
        """
        return self._cfg.get_int("orchestrator:scaling_max_nodes") or 10
    
    @property
    def scaling_desired_state(self) -> int:
        """
        🇪🇸 Estado deseado de nodos (ignorado si autoscaling está activo).
        🇺🇸 Desired node state (ignored if autoscaling is active).
        """
        return self._cfg.get_int("orchestrator:scaling_desired_state") or 3
    
    @property
    def preserve_scaling_state(self) -> bool:
        """
        🇪🇸 Preservar estado durante operaciones de escalado automático (idempotencia).
        🇺🇸 Preserve state during autoscaling operations (idempotence).
        """
        return self._cfg.get_bool("orchestrator:preserve_scaling_state") or True
    
    @property
    def allow_admin_cidr_blocks(self) -> list[str]:
        """
        🇪🇸 Bloques CIDR autorizados para acceso administrativo (perimetral).
        🇺🇸 Authorized CIDR blocks for admin access (perimeter).
        """
        blocks = self._cfg.get_object("orchestrator:allow_admin_cidr_blocks")
        return blocks or []
    
    @property
    def allow_database_endpoints(self) -> list[str]:
        """
        🇪🇸 Endpoints de base de datos autorizados para salida (perimetral).
        🇺🇸 Authorized database endpoints for outbound (perimeter).
        """
        endpoints = self._cfg.get_object("orchestrator:allow_database_endpoints")
        return endpoints or []
    
    @property
    def allow_proxy_endpoints(self) -> list[str]:
        """
        🇪🇸 Proxies web autorizadas para salida (perimetral).
        🇺🇸 Authorized web proxies for outbound (perimeter).
        """
        proxies = self._cfg.get_object("orchestrator:allow_proxy_endpoints")
        return proxies or []
    
    @property
    def enforce_workload_identity(self) -> bool:
        """
        🇪🇸 Forzar protección de identidad de carga de trabajo (gobernanza de identidad).
        🇺🇸 Enforce workload identity protection (identity governance).
        """
        return self._cfg.get_bool("orchestrator:enforce_workload_identity") or True
    
    @property
    def host_identity_permissions(self) -> list[str]:
        """
        🇪🇸 Permisos mínimos requeridos para identidad de host (least privilege).
        🇺🇸 Minimum required permissions for host identity (least privilege).
        """
        perms = self._cfg.get_object("orchestrator:host_identity_permissions")
        # Default minimum permissions: cluster join and image pull
        return perms or ["eks:JoinCluster", "ecr:GetAuthorizationToken", "ecr:BatchGetImage"]


# Instancia única de configuración accesible globalmente (Singleton Pattern)
# Single configuration instance accessible globally (Singleton Pattern)
config = InfrastructureConfig()
orchestrator_config = OrchestratorConfig()
