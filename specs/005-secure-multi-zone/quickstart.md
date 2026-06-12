# Quickstart: Secure Compute Data Plane Validation

## Prerequisites
- Pulumi CLI installed and configured.
- Access to a development cloud environment (AWS/Azure/GCP).
- Project dependencies installed (`pip install -r requirements.txt`).

## Validation Scenarios

### Scenario 1: Provision Multi-Zone Data Plane
1. Update `infra/config.py` with valid private subnet IDs in at least two different availability zones.
2. Instantiate the `OrchestratorComponent` for the target provider using `OrchestratorProviderFactory`.
3. Run `pulumi up`.
4. **Expected Outcome**: Resources are created within private subnets; no public IPs are assigned to compute nodes.

### Scenario 2: Verify Perimeter Security
1. Attempt to SSH into a compute node from an unauthorized IP.
2. **Expected Outcome**: Connection is dropped instantly (Time-out).

### Scenario 3: Verify Idempotency
1. Increase host count manually in the cloud console.
2. Run `pulumi up` again.
3. **Expected Outcome**: Pulumi reports "no changes" to the host count, preserving the manually scaled nodes.

## Test Commands
- Run mock-based unit tests: `pytest tests/orchestrator/`
