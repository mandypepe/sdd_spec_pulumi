# Quickstart: K8s Base Infrastructure

## Prerequisites
- Validated multi-zone VPC networks available.
- Secure web translation gateways provisioned.
- Pulumi CLI installed and configured.
- Access to target cloud provider credentials.

## Validation Scenarios

### 1. Provision Cluster
To provision the K8s orchestrator infrastructure, run:
```bash
pulumi up --yes
```

### 2. Verify Private Networking
Inspect the provisioned infrastructure:
- Ensure all nodes in `ComputeNodePool` have exclusively private IP addresses.
- Verify no public IP address resource exists for the node instances.

### 3. Verify Security Isolation
- Attempt an SSH connection from an external public IP to a compute node. Expected outcome: Connection timeout/dropped.
- Verify security group/firewall rule blocking port 22/incoming admin traffic from the internet.

### 4. Verify Log Compliance
- Check the `SecurityLogBucket` configuration to ensure 90-day retention and WORM (Object Lock/Immutable) policy are applied.
