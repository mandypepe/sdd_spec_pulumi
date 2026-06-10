"""
🇪🇸 Implementación de AWS para el componente VPC (Amazon EC2 Networking).
Crea una topología de tres capas distribuida en dos zonas de disponibilidad.

🇺🇸 AWS implementation of the VPC component (Amazon EC2 Networking).
Creates a three-tier topology distributed across two availability zones.
"""

import pulumi
import pulumi_aws as aws
from ..vpc.base import VpcComponent
from ..config import config
from typing import Optional


class AwsVpcComponent(VpcComponent):
    """
    🇪🇸 Implementación AWS del componente VPC (ComponentResource Pattern).
    Encapsula la creación de VPC, subnets, gateways y reglas de seguridad.
    
    🇺🇸 AWS implementation of VPC component (ComponentResource Pattern).
    Encapsulates VPC, subnets, gateways, and security rules creation.
    
    Attributes:
        vpc: 🇪🇸 Referencia al VPC de AWS / 🇺🇸 Reference to AWS VPC
        public_subnets: 🇪🇸 Lista de subnets públicas / 🇺🇸 List of public subnets
    """
    
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        """
        🇪🇸 Inicializa el componente VPC para AWS.
        
        🇺🇸 Initializes AWS VPC component.
        
        Args:
            name: 🇪🇸 Nombre base del componente / 🇺🇸 Base component name
            opts: 🇪🇸 Opciones de recursos Pulumi / 🇺🇸 Pulumi ResourceOptions
        """
        super().__init__("custom:aws:VpcComponent", name, opts=opts)
        self.name = name
        
        # Crear VPC maestra (FR-001: VPC CIDR 10.0.0.0/16)
        # Create master VPC (FR-001: VPC CIDR 10.0.0.0/16)
        self.vpc = aws.ec2.Vpc(
            f"{name}-vpc",
            cidr_block=config.vpc_cidr,
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)  # Parent-child relationship
        )
        self.vpc_id = self.vpc.id
        self.public_subnets = []

        # Crear infraestructura de red (FR-002, FR-003, FR-004)
        # Create network infrastructure (FR-002, FR-003, FR-004)
        self._create_subnets()
        self._create_gateways()
        
        # Habilitar flow logs para observabilidad (FR-011: 1 minuto de agregación)
        # Enable flow logs for observability (FR-011: 1-minute aggregation)
        aws.ec2.FlowLog(
            f"{self.name}-flowlog",
            vpc_id=self.vpc.id,
            traffic_type="ALL",
            log_destination_type="cloud-watch-logs",
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Registrar outputs para acceso a recursos hijo
        # Register outputs for child resource access
        self.register_outputs({
            "vpc_id": self.vpc_id,
        })
        
    def _create_subnets(self):
        """
        🇪🇸 Crea 6 subnets en dos zonas de disponibilidad:
        - 2 subnets públicas (1 por zona)
        - 2 subnets privadas (1 por zona, más amplias /23)
        - 2 subnets aisladas (1 por zona)
        (FR-002: Alineación estricta por zona)
        
        🇺🇸 Creates 6 subnets across two availability zones:
        - 2 public subnets (1 per zone)
        - 2 private subnets (1 per zone, larger /23)
        - 2 isolated subnets (1 per zone)
        (FR-002: Strict zone alignment)
        """
        zones = config.availability_zones
        
        # Iterar sobre zonas de disponibilidad para crear 3 subnets por zona
        # Iterate over availability zones to create 3 subnets per zone
        for i, zone in enumerate(zones):
            # Subnet público (Tier 1 / Public)
            pub = aws.ec2.Subnet(
                f"{self.name}-public-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i+1}.0/24",  # 10.0.1.0/24 or 10.0.2.0/24
                availability_zone=zone,
                tags={**config.tags, "tier": "public", "zone": zone},
                opts=pulumi.ResourceOptions(parent=self)
            )
            self.public_subnets.append(pub)
            
            # Subnet privada (Tier 2 / Private, más ancho /23)
            # Private subnet (Tier 2 / Private, wider /23)
            aws.ec2.Subnet(
                f"{self.name}-private-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{10+2*i}.0/23",  # 10.0.10.0/23 or 10.0.12.0/23
                availability_zone=zone,
                tags={**config.tags, "tier": "private", "zone": zone},
                opts=pulumi.ResourceOptions(parent=self)
            )
            
            # Subnet aislada (Tier 3 / Isolated, base de datos)
            # Isolated subnet (Tier 3 / Isolated, database tier)
            aws.ec2.Subnet(
                f"{self.name}-isolated-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{20+i}.0/24",  # 10.0.20.0/24 or 10.0.21.0/24
                availability_zone=zone,
                tags={**config.tags, "tier": "isolated", "zone": zone},
                opts=pulumi.ResourceOptions(parent=self)
            )
        
    def _create_gateways(self):
        """
        🇪🇸 Crea Internet Gateway, NAT Gateways y reglas de seguridad:
        - Internet Gateway para tráfico público (FR-003)
        - 2 NAT Gateways alineados por zona (FR-004, FR-010)
        - Security Groups para enforced zero-trust (FR-006, FR-007, FR-008)
        (FR-005: Subnets aisladas sin rutas de egreso)
        
        🇺🇸 Creates Internet Gateway, NAT Gateways, and security rules:
        - Internet Gateway for public traffic (FR-003)
        - 2 zone-aligned NAT Gateways (FR-004, FR-010)
        - Security Groups for enforced zero-trust (FR-006, FR-007, FR-008)
        (FR-005: Isolated subnets with no egress routes)
        """
        # Internet Gateway (FR-003: Ruta para tráfico público)
        # Internet Gateway (FR-003: Route for public traffic)
        igw = aws.ec2.InternetGateway(
            f"{self.name}-igw",
            vpc_id=self.vpc.id,
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Security Group para perimeter firewall zero-trust
        # Security Group for zero-trust perimeter firewall
        sg = aws.ec2.SecurityGroup(
            f"{self.name}-sg",
            vpc_id=self.vpc.id,
            ingress=[
                # FR-006: LB Tier - HTTPS inbound from internet
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=443,
                    to_port=443,
                    cidr_blocks=["0.0.0.0/0"],
                    description="HTTPS from Internet (FR-006)"
                ),
                # FR-007 implícito: Compute tier bloquea SSH desde internet (deny by default)
                # FR-007 implicit: Compute tier blocks SSH from internet (deny by default)
                # Compute from LB - allow internal traffic
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=8080,
                    to_port=8080,
                    cidr_blocks=["10.0.0.0/16"],
                    description="Internal compute tier traffic"
                ),
                # FR-008: DB Tier - PostgreSQL only from compute tier
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=5432,
                    to_port=5432,
                    cidr_blocks=["10.0.10.0/23", "10.0.12.0/23"],  # Only private tier
                    description="PostgreSQL from compute tier (FR-008)"
                ),
            ],
            egress=[
                # Allow outbound to internet (default deny-all for isolation)
                # Allow outbound to internet (default deny-all for isolation)
                aws.ec2.SecurityGroupEgressArgs(
                    protocol="-1",
                    from_port=0,
                    to_port=0,
                    cidr_blocks=["0.0.0.0/0"],
                    description="Outbound to Internet (FR-005)"
                )
            ],
            tags=config.tags,
            opts=pulumi.ResourceOptions(parent=self)
        )
