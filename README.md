# Pulumi Multi-Cloud Infrastructure Base

---

## 🇪🇸 Descripción (Español)

Este proyecto implementa una base de infraestructura multi-cloud (AWS, Azure, GCP) utilizando Pulumi y siguiendo las mejores prácticas de ingeniería de software. El objetivo es proporcionar un estándar de oro para la infraestructura como código (IaC), siendo modular, testeable y fácil de extender.

### Arquitectura y Principios

- **Patrón Factory**: Utilizado en `infra/providers.py` para instanciar componentes según el proveedor seleccionado. Cumple con el principio Open/Closed (OCP).
- **ComponentResource**: Todos los recursos se agrupan en componentes lógicos, facilitando la organización y el seguimiento de dependencias (Parent/Child).
- **Configuración Tipada**: La clase `InfrastructureConfig` en `infra/config.py` centraliza y valida todos los parámetros de entrada.
- **SOLID**: 
    - **SRP**: Cada módulo y clase tiene una única responsabilidad.
    - **OCP**: Es fácil añadir nuevos proveedores sin modificar la fábrica central.
    - **LSP/ISP/DIP**: Uso de clases base abstractas e inyección de dependencias.

### Estructura del Proyecto

```text
.
├── infra/
│   ├── vpn/                # VPN implementations
│   ├── lb/                 # Load Balancer implementations
│   ├── orchestrator/       # Multi-zone Orchestrator implementations
│   ├── vpc/                # VPC implementations
│   ├── config.py           # Typed configuration management
│   ├── constants.py        # Constant values and CIDRs
│   └── providers.py        # Component Factory
├── tests/                  # Unit testing suite with mocks
├── main.py                 # Pulumi entry point
└── requirements.txt        # Project dependencies
```

### Ramas de Desarrollo (Branches)

Resumen de la evolución y propósitos de las ramas del proyecto:

- `main`: Infraestructura base multi-cloud.
- `create_constitution`: Configuración inicial y normalización de archivos.
- `install_spec_kit`: Integración de la metodología de desarrollo dirigida por especificaciones.
- `002-agnostic-vpc-topology`: Implementación de topologías de VPC agnósticas.
- `003_agnostic_external-lb-security`: Implementación de balanceadores de carga externos y políticas de seguridad.
- `004-k8s-base-infra`: Infraestructura base para Kubernetes.
- `005-secure-multi-zone`: Configuración de entornos multi-zona seguros.
- `006-secure-container-registry`: Implementación de registro de contenedores seguro.

### Gestión de Especificaciones y Gobernanza

- **`dtls/`**: Contiene especificaciones técnicas, documentos de diseño y lógica de alto nivel.
- **`specs/`**: Contiene la documentación específica de cada característica, incluyendo modelos de datos, planes de implementación, tareas, requisitos de seguridad y contratos.

### Pruebas Unitarias

El proyecto incluye una suite de pruebas que utiliza los mocks de Pulumi, permitiendo validar la lógica sin credenciales reales.

```bash
# Configurar PYTHONPATH para incluir el directorio raíz
$env:PYTHONPATH = "."
pytest
```

---

## 🇺🇸 Description (English)

This project implements a multi-cloud infrastructure base (AWS, Azure, GCP) using Pulumi, following software engineering best practices. The goal is to provide a "gold standard" for Infrastructure as Code (IaC), being modular, testable, and easy to extend.

### Architecture and Principles

- **Factory Pattern**: Used to instantiate components based on the selected provider. Adheres to Open/Closed Principle (OCP).
- **ComponentResource**: Group resources into logical components for organization and dependency tracking.
- **Typed Configuration**: Centralized validation of input parameters.
- **SOLID**: 
    - **SRP**: Single responsibility per module.
    - **OCP**: Easily add new providers.
    - **LSP/ISP/DIP**: Abstract base classes and dependency injection.

### Project Structure

```text
.
├── infra/
│   ├── vpn/                # VPN implementations (base, aws, azure, gcp)
│   ├── lb/                 # Load Balancer implementations (base, aws, azure, gcp)
│   ├── orchestrator/       # Multi-zone Orchestrator implementations (base, aws, azure, gcp)
│   ├── vpc/                # VPC implementations (base, aws, azure, gcp)
│   ├── config.py           # Typed configuration management
│   ├── constants.py        # Constant values and CIDRs
│   └── providers.py        # Component Factory
├── tests/                  # Unit testing suite with mocks
├── main.py                 # Pulumi entry point
└── requirements.txt        # Project dependencies
```

### Development Branches

Summary of the evolution and purpose of project branches:

- `main`: Core multi-cloud infrastructure base.
- `create_constitution`: Initial configuration and file normalization.
- `install_spec_kit`: Integration of spec-driven development methodology.
- `002-agnostic-vpc-topology`: Implementation of agnostic VPC topologies.
- `003_agnostic_external-lb-security`: Implementation of external load balancers and security policies.
- `004-k8s-base-infra`: Kubernetes base infrastructure.
- `005-secure-multi-zone`: Secure multi-zone environment configuration.
- `006-secure-container-registry`: Implementation of secure container registry.

### Specifications and Governance Management

- **`dtls/`**: Contains technical specifications, design documents, and high-level logic documentation.
- **`specs/`**: Contains specific feature-driven documentation, including data models, implementation plans, task breakdowns, security requirements, and architectural contracts.

### Unit Testing

The project includes a testing suite that utilizes Pulumi mocks to validate resource creation logic.

```bash
# Set PYTHONPATH to include the root directory
$env:PYTHONPATH = "."
pytest
```

### 🎯 VPC Component
The VPC module provides abstract-factory-driven infrastructure foundation for multi-zone network isolation across clouds.

- **Features**: Subnet creation (Public/Private/Isolated), Gateway management, and static layout validation.
- **Usage**: Inherit from `VpcComponent` and implement `_create_subnets` and `_create_gateways`.

### 🎯 Load Balancer Component
The Load Balancer module provides a unified interface for defining public ingress points across clouds.

- **Features**: Abstracted load balancer provisioning, HTTPS listener setup, and target group definition.
- **Usage**: Inherit from `LbComponent` and implement `_create_load_balancer`, `_create_listener`, and `_create_target_group`.

### 🎯 Orchestrator Component
The orchestrator module provides factory-driven, multi-cloud infrastructure automation for Kubernetes compute data planes with built-in security.

- **Key Features**: Multi-zone isolation, automated scaling, perimeter security enforcement (blocking unauthorized SSH/RDP), and minimum-privilege identity governance.

### 🚀 How to Extend

1.  Create `infra/<component>/<provider>_<component>.py` inheriting from the base class.
2.  Register the new class in the respective `ProviderFactory` in `infra/providers.py`.
