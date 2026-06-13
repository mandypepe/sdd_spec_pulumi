# Quickstart: Perimeter Security Validation

## Overview
This guide provides a sequence of commands and tests to verify the three-tier isolation and security perimeters.

## Prerequisites
- Pulumi CLI installed.
- Cloud provider credentials (AWS, Azure, or GCP).
- Project initialized with `pulumi up`.

## Validation Scenarios

### 1. Public Entry Validation (P1)
**Goal**: Verify only HTTPS is allowed to the public tier.
```bash
# Attempt to reach public LB on port 80 (Should fail)
curl -v http://<public-lb-ip>

# Attempt to reach public LB on port 443 (Should succeed)
curl -vk https://<public-lb-ip>
```

### 2. Administrative Lockout (P2)
**Goal**: Verify SSH is blocked from the internet.
```bash
# Attempt to SSH into a compute node from external IP (Should timeout)
ssh -i key.pem ubuntu@<compute-node-ip>
```

### 3. Data Tier Isolation (P3)
**Goal**: Verify database is only reachable from the compute tier.
```bash
# From a machine OUTSIDE the compute tier (Should fail)
psql -h <db-endpoint> -U user -d db

# From a node INSIDE the compute tier (Should succeed)
# (Assumes psql installed on node or simulated via test container)
kubectl exec -it <pod-name> -- psql -h <db-endpoint> -U user -d db
```

### 4. Zero-Outbound Data Tier (P3)
**Goal**: Verify database cannot reach the internet.
```bash
# From the database host/instance (if shell access available for testing)
# or via managed service metric check.
ping 8.8.8.8 # Should fail 100%
```

### 5. Lifecycle Protection (P4)
**Goal**: Verify perimeters cannot be accidentally deleted.
```bash
# Attempt to delete the security group/NSG manually or via Pulumi
pulumi destroy --target "urn:pulumi:stack::project::custom:aws:SecurityPerimeter::data"
# Expected Outcome: Error "cannot delete resource because it is protected"
```

## Audit Log Verification
**Goal**: Confirm logs are captured and retention is set.
```bash
# AWS: Verify retention policy
aws logs describe-log-groups --log-group-name-prefix "/aws/vpc/flow-logs" \
  --query "logGroups[0].retentionInDays"
# Expected: 365
```
