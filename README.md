# Pulumi Multi-Cloud VPN Infrastructure

---

## 🇪🇸 Descripción (Español)

Este proyecto implementa una base de infraestructura para VPNs multi-cloud (AWS, Azure, GCP) utilizando Pulumi y siguiendo las mejores prácticas de ingeniería de software. El objetivo es proporcionar un estándar de oro para la infraestructura como código (IaC), siendo modular, testeable y fácil de extender.

### Arquitectura y Principios

- **Patrón Factory**: Utilizado en `infra/providers.py` para instanciar el componente VPN correcto según el proveedor seleccionado. Cumple con el principio Open/Closed (OCP).
- **ComponentResource**: Todos los recursos se agrupan en componentes lógicos, facilitando la organización y el seguimiento de dependencias (Parent/Child).
- **Configuración Tipada**: La clase `InfrastructureConfig` en `infra/config.py` centraliza y valida todos los parámetros de entrada.
- **SOLID**: 
    - **SRP**: Cada módulo y clase tiene una única responsabilidad.
    - **OCP**: Es fácil añadir nuevos proveedores sin modificar la fábrica central.
    - **LSP/ISP/DIP**: Uso de clases base abstractas (`VpnComponent`) e inyección de dependencias a través de opciones de Pulumi.

### Estructura del Proyecto

```text
.
├── infra/
│   ├── vpn/                # Implementaciones específicas por nube
│   │   ├── base.py         # Interfaz abstracta
│   │   ├── aws_vpn.py
│   │   ├── azure_vpn.py
│   │   └── gcp_vpn.py
│   ├── config.py           # Gestión de configuración tipada
│   ├── constants.py        # Valores constantes y CIDRs
│   └── providers.py        # Fábrica de componentes (Factory Pattern)
├── tests/                  # Suite de pruebas unitarias con mocks
├── main.py                 # Punto de entrada de Pulumi
└── requirements.txt        # Dependencias del proyecto
```

### Pruebas Unitarias

El proyecto incluye una suite de pruebas que utiliza los mocks de Pulumi, permitiendo validar la lógica de creación de recursos sin necesidad de credenciales reales de la nube.

Para ejecutar las pruebas:

```bash
# Configurar PYTHONPATH para incluir el directorio raíz
$env:PYTHONPATH = "."
pytest
```

---

## 🇺🇸 Description (English)

This project implements an infrastructure base for multi-cloud VPNs (AWS, Azure, GCP) using Pulumi, following software engineering best practices. The goal is to provide a "gold standard" for Infrastructure as Code (IaC), being modular, testable, and easy to extend.

### Architecture and Principles

- **Factory Pattern**: Used in `infra/providers.py` to instantiate the correct VPN component based on the selected provider. It adheres to the Open/Closed Principle (OCP).
- **ComponentResource**: All resources are grouped into logical components, facilitating organization and dependency tracking (Parent/Child).
- **Typed Configuration**: The `InfrastructureConfig` class in `infra/config.py` centralizes and validates all input parameters.
- **SOLID**:
    - **SRP**: Every module and class has a single responsibility.
    - **OCP**: It is easy to add new providers without modifying the central factory.
    - **LSP/ISP/DIP**: Use of abstract base classes (`VpnComponent`) and dependency injection via Pulumi options.

### Project Structure

```text
.
├── infra/
│   ├── vpn/                # Cloud-specific implementations
│   │   ├── base.py         # Abstract interface
│   │   ├── aws_vpn.py
│   │   ├── azure_vpn.py
│   │   └── gcp_vpn.py
│   ├── lb/                 # Public Load Balancer implementations
│   │   ├── base.py
│   │   ├── aws_lb.py
│   │   ├── azure_lb.py
│   │   └── gcp_lb.py
│   ├── orchestrator/       # Multi-zone Orchestrator implementations
│   │   ├── base.py         # Abstract orchestrator interface with security & identity
│   │   ├── aws_k8s.py      # AWS Kubernetes orchestrator
│   │   ├── azure_k8s.py    # Azure Kubernetes orchestrator
│   │   └── gcp_k8s.py      # GCP Kubernetes orchestrator
│   ├── config.py           # Typed configuration management
│   ├── constants.py        # Constant values and CIDRs
│   └── providers.py        # Component Factory (Factory Pattern)
├── tests/                  # Unit testing suite with mocks
├── main.py                 # Pulumi entry point
└── requirements.txt        # Project dependencies
```

### Unit Testing

The project includes a testing suite that utilizes Pulumi mocks, allowing for validation of resource creation logic without requiring real cloud credentials.

To run the tests:

```bash
# Set PYTHONPATH to include the root directory
$env:PYTHONPATH = "."
pytest
```

### 🎯 Orchestrator Component (HU-004: Secure Multi-Zone Automated Compute Data Plane)

**Overview**: The orchestrator module provides factory-driven, multi-cloud infrastructure automation for Kubernetes compute data planes with built-in security, multi-zone isolation, and identity governance.

#### Key Features

- **Multi-Zone Private Network Isolation** (User Story 1)
  - Automatically distributes compute infrastructure across multiple availability zones
  - Ensures all compute nodes reside in private, non-routable subnets
  - Prevents public internet access to compute nodes

- **Automated Scaling Synchronization** (User Story 2)
  - Preserves live node count during infrastructure updates
  - Implements idempotent state management
  - Prevents disruption to active workloads during deployments

- **Perimeter Security Enforcement** (User Story 3)
  - Blocks unauthorized remote access (SSH/RDP) from public internet
  - Restricts egress traffic to authorized destinations only
  - Supports DNS, database, and proxy endpoints
  - Automatically configured security groups/firewall rules per provider

- **Minimum Privilege Identity Governance** (User Story 4)
  - Assigns least-privilege IAM roles/service accounts to compute hosts
  - Enforces workload identity protection
  - Prevents access to sensitive business data

#### Usage Example

```python
from infra.orchestrator import OrchestratorProviderFactory

# Instantiate orchestrator for target cloud provider
orchestrator = OrchestratorProviderFactory.get_component("aws", "compute-plane")

# Configure multi-zone isolation
zones = ["us-east-1a", "us-east-1b"]
subnets = ["subnet-11111", "subnet-22222"]
orchestrator.allocate_multi_zone_subnets(zones, subnets)

# Configure security
orchestrator.configure_security()

# Configure identity
orchestrator.configure_identity()

# Provision infrastructure
orchestrator.provision()
```

#### Testing

All orchestrator components include comprehensive mock-based unit tests:

```bash
# Run orchestrator tests only
pytest tests/orchestrator/ -v

# Run specific cloud provider tests
pytest tests/orchestrator/test_aws_k8s.py -v
pytest tests/orchestrator/test_azure_k8s.py -v
pytest tests/orchestrator/test_gcp_k8s.py -v
```

---

## 🚀 Cómo Extender / How to Extend

1.  **🇪🇸 ES**: Crea `infra/vpn/oracle_vpn.py` heredando de `VpnComponent`. Registra la clase en `VpnProviderFactory`.
2.  **🇺🇸 EN**: Create `infra/vpn/oracle_vpn.py` inheriting from `VpnComponent`. Register the class in `VpnProviderFactory`.
