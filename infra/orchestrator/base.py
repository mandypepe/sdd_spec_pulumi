import pulumi
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, List

class OrchestratorComponent(pulumi.ComponentResource, ABC):
    """
    🇪🇸 Componente base abstracto para orquestadores Kubernetes con soporte para:
    - Multi-zona con aislamiento de red privada (User Story 1)
    - Preservación de estado durante escalado automático (User Story 2)
    - Perimetro restringido y seguridad perimetral (User Story 3)
    - Gobernanza de identidad con privilegios mínimos (User Story 4)
    
    🇺🇸 Abstract base component for Kubernetes orchestrators with support for:
    - Multi-zone private network isolation (User Story 1)
    - State preservation during autoscaling (User Story 2)
    - Restricted perimeter and perimeter security (User Story 3)
    - Identity governance with minimum privilege (User Story 4)
    """
    def __init__(self, resource_type: str, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__(resource_type, name, opts=opts)
        self._availability_zones: List[str] = []
        self._subnet_ids: List[str] = []
        self._scaled_node_count: Optional[int] = None
        self._perimeter_rules: Dict[str, any] = {}
        self._identity_permissions: List[str] = []

    # ==================== User Story 1: Multi-Zone Isolation ====================
    
    @abstractmethod
    def provision(self):
        """Provision orchestrator and node pools across multiple zones"""
        pass

    @abstractmethod
    def allocate_multi_zone_subnets(self, availability_zones: List[str], subnet_ids: List[str]) -> Dict[str, str]:
        """
        🇪🇸 Asignar subnets privadas a zonas de disponibilidad para aislamiento multi-zona.
        🇺🇸 Allocate private subnets to availability zones for multi-zone isolation.
        
        Returns: Mapping of zone -> subnet_id
        """
        pass

    # ==================== User Story 2: Scaling Synchronization ====================
    
    @abstractmethod
    def get_current_node_count(self) -> int:
        """
        🇪🇸 Obtener el número actual de nodos orquestados (estado en vivo).
        🇺🇸 Get the current number of orchestrated nodes (live state).
        """
        pass

    def preserve_scaling_state(self, desired_count: int) -> bool:
        """
        🇪🇸 Preservar estado de escalado actual: ignorar diferencias en conteo de nodos.
        Idempotencia: si actual > deseado (autoscaled), mantener actual.
        
        🇺🇸 Preserve current scaling state: ignore differences in node count.
        Idempotence: if actual > desired (autoscaled), keep actual.
        
        Returns: True if state was preserved (no changes needed), False if sync needed
        """
        current = self.get_current_node_count()
        self._scaled_node_count = current
        if current > desired_count:
            pulumi.info(f"Preserving scaled state: current={current} > desired={desired_count}")
            return True
        return False

    # ==================== User Story 3: Perimeter Enforcement ====================
    
    @abstractmethod
    def configure_security(self):
        """Configure perimeter security: Block admin ports, secure translation gateways"""
        pass

    def configure_ingress_rules(self, allow_admin_cidr_blocks: List[str]) -> Dict[str, any]:
        """
        🇪🇸 Configurar reglas de entrada: bloquear acceso administrativo no autorizado.
        🇺🇸 Configure ingress rules: block unauthorized admin access.
        
        Returns: Security group/firewall rules for ingress
        """
        rules = {
            "block_all_ssh": {
                "protocol": "tcp",
                "from_port": 22,
                "to_port": 22,
                "cidr_blocks": [],
                "description": "Block SSH from public internet"
            },
            "block_all_rdp": {
                "protocol": "tcp",
                "from_port": 3389,
                "to_port": 3389,
                "cidr_blocks": [],
                "description": "Block RDP from public internet"
            },
            "allow_lb_traffic": {
                "protocol": "tcp",
                "from_port": 30000,
                "to_port": 32767,
                "cidr_blocks": ["0.0.0.0/0"],  # Load balancer traffic
                "description": "Allow NodePort traffic from load balancer"
            }
        }
        
        if allow_admin_cidr_blocks:
            rules["allow_admin_ssh"] = {
                "protocol": "tcp",
                "from_port": 22,
                "to_port": 22,
                "cidr_blocks": allow_admin_cidr_blocks,
                "description": "Allow SSH from authorized admin zones only"
            }
        
        self._perimeter_rules["ingress"] = rules
        return rules

    def configure_egress_rules(self, database_endpoints: List[str], proxy_endpoints: List[str]) -> Dict[str, any]:
        """
        🇪🇸 Configurar reglas de salida: restringir solo a bases de datos y proxies autorizados.
        🇺🇸 Configure egress rules: restrict to authorized database and proxy endpoints only.
        
        Returns: Security group/firewall rules for egress
        """
        rules = {
            "deny_all_outbound": {
                "protocol": "-1",
                "from_port": 0,
                "to_port": 65535,
                "cidr_blocks": ["0.0.0.0/0"],
                "description": "Deny all outbound by default"
            },
            "allow_database": {
                "protocol": "tcp",
                "from_port": 5432,  # PostgreSQL
                "to_port": 5432,
                "destinations": database_endpoints,
                "description": "Allow outbound to authorized database endpoints only"
            },
            "allow_proxy": {
                "protocol": "tcp",
                "from_port": 80,
                "to_port": 443,
                "destinations": proxy_endpoints,
                "description": "Allow outbound to authorized web proxies only"
            },
            "allow_dns": {
                "protocol": "udp",
                "from_port": 53,
                "to_port": 53,
                "destinations": ["0.0.0.0/0"],
                "description": "Allow DNS resolution"
            }
        }
        
        self._perimeter_rules["egress"] = rules
        return rules

    # ==================== User Story 4: Identity Governance ====================
    
    @abstractmethod
    def configure_identity(self):
        """Configure federated identity: OIDC/Token provider, least privilege IAM"""
        pass

    def configure_minimum_privilege_identity(self, permissions: List[str]) -> Dict[str, any]:
        """
        🇪🇸 Configurar identidad con privilegios mínimos: solo permisos necesarios.
        🇺🇸 Configure minimum privilege identity: only required permissions.
        
        Args:
            permissions: List of minimum required action strings
        
        Returns: Identity configuration (IAM policy, service account, etc.)
        """
        self._identity_permissions = permissions
        
        # Default minimum permissions for orchestrator hosts
        default_perms = {
            "cluster_join": "Allow host to register with orchestrator cluster",
            "image_pull": "Allow pulling approved container images from registry",
            "metrics_report": "Allow reporting metrics to monitoring system",
            "secret_read": "Allow reading cluster join token only"
        }
        
        identity_config = {
            "permissions": permissions or list(default_perms.keys()),
            "deny_business_data": True,
            "deny_cross_account": True,
            "enforce_workload_identity": True,
            "description": "Restricted host identity with minimum privilege"
        }
        
        return identity_config

    @abstractmethod
    def get_identity_arn_or_id(self) -> str:
        """
        🇪🇸 Obtener el ARN/ID de la identidad de host para auditoría.
        🇺🇸 Get host identity ARN/ID for audit.
        """
        pass

class OrchestratorProviderFactory:
    """
    🇪🇸 Fábrica para instanciar componentes de orquestador basados en el proveedor.
    🇺🇸 Factory to instantiate orchestrator components based on provider.
    """
    _providers: Dict[str, Type[OrchestratorComponent]] = {}

    @classmethod
    def register(cls, provider: str, component_class: Type[OrchestratorComponent]):
        cls._providers[provider.lower()] = component_class

    @classmethod
    def get_component(cls, provider: str, name: str, opts: pulumi.ResourceOptions = None) -> OrchestratorComponent:
        component_class = cls._providers.get(provider.lower())
        if not component_class:
            raise ValueError(f"Provider '{provider}' not registered.")
        return component_class(name, opts=opts)
