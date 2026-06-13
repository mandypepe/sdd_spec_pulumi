# Pulumi Multi-Cloud Infrastructure Framework

---

## 🇪🇸 Descripción (Español)

Este proyecto implementa una base de infraestructura multi-cloud (AWS, Azure, GCP) utilizando Pulumi y siguiendo las mejores prácticas de ingeniería de software. El objetivo es proporcionar un estándar de oro para la infraestructura como código (IaC), siendo modular, testeable y fácil de extender para topologías de red, balanceadores de carga, orquestación de Kubernetes, registros de contenedores y bases de datos administradas.

El proyecto incorpora un enfoque riguroso de **desarrollo dirigido por especificaciones (Spec-Driven Development)**, gestionando el ciclo de vida de las características desde su conceptualización técnica hasta su implementación verificada.

### Arquitectura y Principios

- **Patrón Factory**: Utilizado en `infra/providers.py` para instanciar componentes según el proveedor seleccionado. Cumple con el principio Open/Closed (OCP).
- **ComponentResource**: Todos los recursos se agrupan en componentes lógicos de Pulumi, facilitando la organización y el seguimiento de dependencias (Parent/Child).
- **Configuración Tipada**: La clase `InfrastructureConfig` en `infra/config.py` centraliza y valida todos los parámetros de entrada.
- **SOLID**: Diseñado para SRP, OCP, LSP, ISP y DIP.

### Estructura del Proyecto

```text
.
├── .specify/               # Gobernanza, plantillas y seguimiento de flujo de trabajo
├── dtls/                   # Especificaciones de diseño, técnicas y de lógica
├── infra/                  # Componentes de infraestructura (Basados en Factory)
│   ├── vpc/                # Topologías de red agnósticas (Tier-based)
│   ├── lb/                 # Balanceadores de carga externos
│   ├── orchestrator/       # Orquestación de computo (K8s)
│   ├── db/                 # Bases de datos administradas (RDS, Flexible Server, Cloud SQL)
│   ├── registry/           # Registros de contenedores seguros (ECR, ACR, Artifact Registry)
│   ├── vpn/                # Conectividad VPN
│   ├── config.py           # Gestión de configuración tipada
│   └── providers.py        # Fábricas de componentes
├── specs/                  # Especificaciones de características (SDD)
├── tests/                  # Suite de pruebas unitarias con mocks de Pulumi
├── main.py                 # Punto de entrada de Pulumi
└── requirements.txt        # Dependencias del proyecto
```

### Ramas de Desarrollo (Branches)

Resumen de la evolución y los hitos implementados en cada rama:

- `main`: Infraestructura base y arquitectura de referencia multi-cloud.
- `create_constitution`: Definición de la gobernanza del proyecto y principios de ingeniería.
- `install_spec_kit`: Integración de herramientas para el desarrollo dirigido por especificaciones.
- `002-agnostic-vpc-topology`: Arquitectura de red agnóstica con tres capas (Public, Private, Isolated).
- `003_agnostic_external-lb-security`: Balanceadores de carga externos con políticas de seguridad perimetral automáticas.
- `004-k8s-base-infra`: Fundamento del plano de control de Kubernetes multi-nube.
- `005-secure-multi-zone`: Plano de datos de cómputo multi-zona automatizado con gobernanza de identidad.
- `006-secure-container-registry`: Repositorios de contenedores con inmutabilidad de tags y escaneo de vulnerabilidades.
- `006_isolated-managed-database`: Provisión de bases de datos administradas (RDS, Azure PG Flexible, Cloud SQL) en capas de red aisladas.
- `007_network-firewall-isolation`: Reforzamiento de aislamiento de red mediante reglas de firewall granulares.

### 🎯 Componentes Principales

#### Managed Database (HU-006)
Automatización para bases de datos relacionales con aislamiento total, alta disponibilidad multi-zona y cifrado AES-256.

#### Container Registry (HU-005)
Gestión de imágenes de contenedores con políticas de inmutabilidad y escaneo de seguridad integrado.

#### Secure Orchestrator
Plano de cómputo para K8s con aislamiento multi-zona y gestión de identidades bajo el principio de mínimo privilegio.

### Pruebas Unitarias

El proyecto incluye una suite exhaustiva de pruebas que utiliza los mocks de Pulumi.

Para ejecutar todas las pruebas:
```bash
$env:PYTHONPATH = "."
pytest
```

---

## 🇺🇸 Description (English)

This project implements a multi-cloud infrastructure base (AWS, Azure, GCP) using Pulumi, following software engineering best practices. The goal is to provide a "gold standard" for Infrastructure as Code (IaC), being modular, testable, and easy to extend for network topologies, load balancers, Kubernetes orchestration, container registries, and managed databases.

The project incorporates a rigorous **Spec-Driven Development** approach, managing the feature lifecycle from technical conceptualization to verified implementation.

### Architecture and Principles

- **Factory Pattern**: Used in `infra/providers.py` to instantiate components based on the selected provider. Adheres to the Open/Closed Principle (OCP).
- **ComponentResource**: Resources are grouped into logical Pulumi components for organization and dependency management.
- **Typed Configuration**: `InfrastructureConfig` centralizes and validates input parameters.
- **SOLID**: Designed for SRP, OCP, LSP, ISP, and DIP.

### Project Structure

```text
.
├── .specify/               # Governance, templates, and workflow tracking
├── dtls/                   # Design, Technical, and Logic specifications
├── infra/                  # Infrastructure components (Factory-based)
│   ├── vpc/                # Agnostic network topologies (Tier-based)
│   ├── lb/                 # External Load Balancers
│   ├── orchestrator/       # Compute orchestration (K8s)
│   ├── db/                 # Managed Databases (RDS, Flexible Server, Cloud SQL)
│   ├── registry/           # Secure Container Registries (ECR, ACR, Artifact Registry)
│   ├── vpn/                # VPN connectivity
│   ├── config.py           # Typed configuration management
│   └── providers.py        # Component Factories
├── specs/                  # Feature specifications (SDD artifacts)
├── tests/                  # Unit testing suite with Pulumi mocks
├── main.py                 # Pulumi entry point
└── requirements.txt        # Project dependencies
```

### Development Branches

Summary of the evolution and milestones implemented in each branch:

- `main`: Core multi-cloud infrastructure base and reference architecture.
- `create_constitution`: Project governance definition and engineering principles.
- `install_spec_kit`: Integration of spec-driven development tools.
- `002-agnostic-vpc-topology`: Three-tier agnostic network architecture (Public, Private, Isolated).
- `003_agnostic_external-lb-security`: External load balancers with automated perimeter security policies.
- `004-k8s-base-infra`: Multi-cloud Kubernetes control plane foundation.
- `005-secure-multi-zone`: Automated multi-zone compute data plane with identity governance.
- `006-secure-container-registry`: Container repositories with tag immutability and vulnerability scanning.
- `006_isolated-managed-database`: Provisioning of managed databases (RDS, Azure PG Flexible, Cloud SQL) in isolated network layers.
- `007_network-firewall-isolation`: Network isolation reinforcement via granular firewall rules.

### 🎯 Key Components

#### Managed Database
Automation for relational databases with full isolation, multi-zone high availability, and AES-256 encryption.

#### Container Registry
Image management with immutability policies and integrated security scanning.

#### Secure Orchestrator
Kubernetes compute plane with multi-zone isolation and least-privilege identity governance.

### Unit Testing

The project includes a comprehensive testing suite utilizing Pulumi mocks to validate infrastructure logic without requiring real cloud credentials.

To run all tests:
```bash
$env:PYTHONPATH = "."
pytest
```

---

## 🚀 Cómo Extender / How to Extend

Para añadir un nuevo proveedor o componente:
1. Hereda de la clase base correspondiente en `infra/<componente>/base.py`.
2. Implementa las interfaces específicas del proveedor.
3. Registra la nueva implementación en la fábrica correspondiente en `infra/providers.py`.
