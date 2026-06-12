# Quickstart: Validating the External Load Balancer Feature

This guide provides scenarios to validate that the Public Multi-Zone Traffic Routing and Perimeter Security Policy is correctly implemented and operational.

## Prerequisites

- Python 3.11+
- Pulumi CLI
- Access to an AWS, Azure, or GCP environment (for real deployment) or `pytest` (for mock validation).
- A pre-existing VPC with at least two public subnets.
- A pre-existing SSL certificate in the target cloud provider.

## Scenario 1: Mock-Based Logic Validation (Automated)

Run the unit tests to verify that the Pulumi component correctly translates configurations into provider-specific resources.

```bash
# Set up environment
export PYTHONPATH="."

# Run tests for a specific provider
pytest tests/lb/test_aws_lb.py
pytest tests/lb/test_azure_lb.py
pytest tests/lb/test_gcp_lb.py
```

**Expected Outcome**: All tests pass, confirming that:
- Deletion protection is enabled.
- TLS 1.3 policy is selected.
- Health check interval is 15s.
- Security rules only allow port 443 ingress.

## Scenario 2: Infrastructure Dry-Run (Manual)

Verify the infrastructure plan without making actual changes.

```bash
# Select stack
pulumi stack select dev

# Preview changes
pulumi preview
```

**Validation Steps**:
1. Check the `LoadBalancer` (AWS/Azure/GCP) resource in the output.
2. Confirm `protect: true` is set in the resource options.
3. Confirm `enable_deletion_protection` (or equivalent) is `true`.
4. Verify the `Listener` uses port 443 and the specified SSL policy.
5. Verify the `TargetGroup` (or equivalent) has a health check interval of 15s and path `/healthz`.

## Scenario 3: Destructive Operation Safeguard (Manual)

Verify that the un-deletable runtime lifecycle attribute works.

```bash
# Attempt to destroy the stack
pulumi destroy
```

**Expected Outcome**: Pulumi should reject the destruction of the load balancer resource with an error similar to:
`error: cannot destroy resource ... because it is protected`.

## Scenario 4: Connectivity & Security Perimeter (Live)

Once deployed, verify the network boundary.

1. **Successful Access**:
   - `curl -I https://<lb-dns-name>`
   - **Expected**: HTTP 200 or 302 (depending on backend response), connection uses TLS 1.3.

2. **Rejected Access**:
   - `curl -I http://<lb-dns-name>`
   - **Expected**: Connection timeout or rejection (port 80 is not open).

3. **Backend Range Restriction**:
   - Attempt to access a backend node directly on a port outside 30000-32767.
   - **Expected**: Connection rejected by the perimeter filter.
