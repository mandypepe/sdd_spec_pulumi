# Quickstart: VPC Topology Validation

## Prerequisites

- Python 3.11+
- Pulumi CLI
- Cloud Provider Credentials (AWS/Azure/GCP)
- Virtual Environment initialized (`source venv/bin/activate` or `.\venv\Scripts\Activate.ps1`)

## Validation Scenarios

### 1. Mock-Based Unit Testing (Fast Feedback)

Validate the component logic, resource parenting, and CIDR allocations without making real cloud calls.

```bash
# Run VPC specific unit tests
pytest tests/vpc/
```

**Expected Outcome**: All tests pass, confirming that 6 subnets are created with correct CIDRs and are parented to the VPC component.

### 2. Pulumi Dry-Run (Provider Validation)

Perform a simulated deployment to verify that the cloud provider SDKs accept the generated resource configurations.

```bash
# Select a test stack (e.g., dev)
pulumi stack select dev

# Run a dry-run
pulumi preview
```

**Expected Outcome**: Pulumi shows a plan to create 1 VPC, 6 subnets, 1 Internet Gateway, 2 NAT Gateways, and associated routing/firewall rules. No "circular dependency" or "invalid CIDR" errors should appear.

### 3. Isolation Verification

Audit the generated routing tables to ensure the isolated tier has no outbound paths.

```bash
# Export the current stack state
pulumi stack export > state.json

# Check isolated subnet routes for 0.0.0.0/0 destinations
# (Requires manual check or a small script to parse state.json)
```

**Expected Outcome**: Isolated subnets must NOT have any route where `DestinationCidrBlock` is `0.0.0.0/0`.
