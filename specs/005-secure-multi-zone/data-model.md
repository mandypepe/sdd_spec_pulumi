# Data Model: Secure Multi-Zone Automated Compute Data Plane

## Entities

### Compute Tier (OrchestratorComponent)
- **Description**: The high-level component defining the compute data plane.
- **Attributes**:
    - `provider`: (String) e.g., "aws", "azure", "gcp"
    - `availability_zones`: (List[String]) The physical zones to span.
    - `subnet_ids`: (List[String]) Private subnets for the data plane.
    - `scaling_targets`: (ScalingConfiguration) Elastic limits.

### Scaling Configuration
- **Description**: Operational contract for elasticity.
- **Attributes**:
    - `min_size`: (Integer) Minimum compute nodes.
    - `max_size`: (Integer) Maximum compute nodes.
    - `desired_state`: (Integer) Preferred baseline (to be ignored if autoscaled).

### Network Boundary
- **Description**: Defensive perimeter for traffic filtering.
- **Attributes**:
    - `ingress_rules`: (List[Rule]) Explicitly allowed incoming traffic.
    - `egress_rules`: (List[Rule]) Explicitly allowed outgoing traffic.

### Host Identity
- **Description**: Permissions persona for compute hosts.
- **Attributes**:
    - `role_arn` (AWS) / `managed_identity_id` (Azure) / `service_account` (GCP)
    - `permitted_actions`: (List[String]) Minimum required operational actions.
