# AGENTS.md - Pulumi Multi-Cloud VPN Infrastructure

## Architecture Overview

This is a **multi-cloud VPN infrastructure project** using Pulumi (Infrastructure as Code) that implements AWS, Azure, and GCP VPN deployments. The design emphasizes extensibility and testability through SOLID principles and the Factory Pattern.

### Big Picture Data Flow

```
main.py → config (centralized, typed settings)
        → VpnProviderFactory (factory pattern)
           → VpnComponent (abstract base)
              → AwsVpn/AzureVpn/GcpVpn (provider-specific implementations)
                 → Cloud-specific resources (VPC, VNets, Networks)
```

**Key architectural insight**: The factory in `infra/providers.py` eliminates the need to modify core logic when adding new cloud providers—just create a new VPN class and register it in `_PROVIDERS` dict.

## Critical Files & Patterns

### Configuration Management (`infra/config.py`)
- **Centralized, typed configuration** via singleton-style `config` object
- Reads from Pulumi Config (`pulumi.Config()`) first, falls back to environment variables
- Supports cloud-specific regions: `aws_region`, `gcp_region`, `azure_location`
- **Pattern**: Never access `pulumi.Config()` directly—always use the `config` singleton imported from `infra.config`

### Component Hierarchy (`infra/vpn/base.py` → implementation files)
- All VPN implementations inherit from `VpnComponent(pulumi.ComponentResource, ABC)`
- **Must implement**: `get_outputs()` method returning a `Dict[str, Any]`
- **Parent/Child relationship**: Child resources use `pulumi.ResourceOptions(parent=self)` to maintain dependency hierarchy
- **Naming convention**: Resource names use `f"{name}-{resource_type}"` pattern (e.g., `"vpn-vpc"`, `"vpn-vpn-gateway"`)

### Factory Pattern (`infra/providers.py`)
- `VpnProviderFactory.create()` is the single entry point for instantiating VPN components
- Raises `ValueError` with helpful message if provider not in `_PROVIDERS` dict
- Adding a new provider: (1) Create `infra/vpn/new_provider_vpn.py`, (2) Add to `_PROVIDERS` dict

## Developer Workflows

### Running Tests
```bash
# Windows PowerShell - must set PYTHONPATH for relative imports
$env:PYTHONPATH = "."
pytest

# Or with verbose output
pytest -v
```

**Test structure**: `tests/conftest.py` provides `pulumi_mocks` fixture that mocks Pulumi runtime—tests run without cloud credentials.

### Deploying Infrastructure
Tests pass → Pulumi stack configuration → `pulumi up` (actual cloud deployment)

## Project-Specific Conventions

1. **Bilingual documentation**: All docstrings and comments are Spanish (🇪🇸) + English (🇺🇸)
2. **Config precedence**: Pulumi Config (Pulumi.yaml environment vars) overrides OS environment variables
3. **Resource naming**: `{name}-{resource_type}` (e.g., component named "vpn" → VPC named "vpn-vpc")
4. **Tags**: All cloud resources inherit `config.tags` (managed-by: "pulumi", project: "multi-cloud-vpn")
5. **Constants over magic numbers**: CIDR blocks, SKUs, and names stored in `infra/constants.py`

## Integration Points

- **Pulumi runtime**: Via `pulumi.ComponentResource`, `pulumi.ResourceOptions`, `pulumi.export()`
- **Cloud SDKs**: `pulumi_aws`, `pulumi_azure_native`, `pulumi_gcp`
- **Testing**: `pytest`, `pulumi.runtime.Mocks`
- **Project metadata**: PYTHONPATH must include project root for `infra.*` imports

## Common Tasks for AI Agents

**Adding a new VPN provider** (e.g., Oracle):
1. Create `infra/vpn/oracle_vpn.py` inheriting from `VpnComponent`
2. Implement `__init__()` creating provider-specific resources
3. Implement `get_outputs()` returning resource IDs/names
4. Add to `VpnProviderFactory._PROVIDERS` dict
5. Add test case in `tests/test_vpn_factory.py`

**Modifying configuration**: Edit `infra/config.py` (`InfrastructureConfig` class), not scattered across codebase.

**Creating new resources**: Use parent/child relationship: `opts=pulumi.ResourceOptions(parent=self)` in child resources.

## Key Dependencies & Versions
- `pulumi>=3.0.0` (core orchestration)
- `pulumi-aws`, `pulumi_azure_native`, `pulumi-gcp` (provider SDKs)
- `pytest` (testing)
- `ruff` (linting)

## Files NOT to Hand-Edit
- `infra/__pycache__/`, `tests/__pycache__/` (generated)
- `dtls/*.md` (specification documents, reference only)

