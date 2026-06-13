# Pulumi Multi-Cloud Infrastructure Framework

---

## 🇪🇸 Descripción (Español)

Este proyecto implementa una base de infraestructura multi-cloud (AWS, Azure, GCP) utilizando Pulumi y siguiendo las mejores prácticas de ingeniería de software. El objetivo es proporcionar un estándar de oro para la infraestructura como código (IaC), siendo modular, testeable y fácil de extender para topologías de VPC, balanceadores de carga, orquestación de Kubernetes y conectividad VPN.

### Arquitectura y Principios

- **Patrón Factory**: Utilizado en `infra/providers.py` (y fábricas específicas) para instanciar componentes según el proveedor seleccionado. Cumple con el principio Open/Closed (OCP).
- **ComponentResource**: Todos los recursos se agrupan en componentes lógicos de Pulumi, facilitando la organización y el seguimiento de dependencias (Parent/Child).
- **Configuración Tipada**: La clase `InfrastructureConfig` en `infra/config.py` centraliza y valida todos los parámetros de entrada.
- **SOLID**:
    - **SRP**: Cada módulo y clase tiene una única responsabilidad.
    - **OCP**: Es fácil añadir nuevos proveedores sin modificar las fábricas centrales.

### Estructura del Proyecto

```text
.
├── infra/                  # Componentes de infraestructura
│   ├── vpc/                # Topologías de red (VPC)
│   ├── lb/                 # Balanceadores de carga
│   ├── orchestrator/       # Orquestación de computo (K8s)
│   ├── vpn/                # Conectividad VPN
│   ├── config.py           # Gestión de configuración tipada
│   └── providers.py        # Fábricas de componentes
├── specs/                  # Especificaciones (Spec-driven development)
├── tests/                  # Suite de pruebas unitarias con mocks
└── main.py                 # Punto de entrada de Pulumi
```

### Pruebas Unitarias

El proyecto incluye una suite de pruebas que utiliza los mocks de Pulumi, permitiendo validar la lógica de creación de recursos sin necesidad de credenciales reales.

Para ejecutar todas las pruebas:
```bash
$env:PYTHONPATH = "."
pytest
```

---

## 🇺🇸 Description (English)

This project implements a multi-cloud infrastructure base (AWS, Azure, GCP) using Pulumi, following software engineering best practices. The goal is to provide a "gold standard" for Infrastructure as Code (IaC), being modular, testable, and easy to extend for VPC topologies, load balancers, Kubernetes orchestration, and VPN connectivity.

### Architecture and Principles

- **Factory Pattern**: Used across components to instantiate cloud-specific resources adhering to the Open/Closed Principle (OCP).
- **ComponentResource**: Resources are grouped into logical Pulumi components for organization and dependency management.
- **Typed Configuration**: `InfrastructureConfig` centralizes and validates input parameters.
- **SOLID**: Designed for SRP, OCP, LSP, ISP, and DIP.

### Project Structure

```text
.
├── infra/                  # Infrastructure components
│   ├── vpc/                # Virtual Private Cloud topologies
│   ├── lb/                 # Load Balancer implementations
│   ├── orchestrator/       # Compute orchestration (K8s)
│   ├── vpn/                # VPN connectivity
│   ├── config.py           # Typed configuration management
│   └── providers.py        # Component Factories
├── specs/                  # Specification-driven development artifacts
├── tests/                  # Unit testing suite with mocks
└── main.py                 # Pulumi entry point
```

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
