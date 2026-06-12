# Data Model: Public Multi-Zone Traffic Routing and Perimeter Security Policy

## Entities

### LbComponent (ComponentResource)
The base abstraction for the Load Balancer component.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `vpc_id` | `Output[str]` | ID of the VPC where the LB is deployed. | Required |
| `public_subnet_ids` | `Output[list[str]]` | List of public subnet IDs for the LB. | Min 2 zones (multi-zone) |
| `certificate_arn_or_id` | `str` | Reference to the pre-existing SSL certificate. | Required |
| `backend_port_range` | `tuple[int, int]` | Port range for backend compute nodes. | Default: (30000, 32767) |
| `health_check_path` | `str` | URL path for health checks. | Default: "/healthz" |
| `health_check_interval` | `int` | Interval in seconds between checks. | Default: 15, Max: 15 |
| `enable_deletion_protection` | `bool` | Whether to protect resources from deletion. | Default: True |

### PerimeterTrafficFilter (Security Group / NSG / Firewall)
Defines the boundary security rules.

| Rule | Direction | Protocol | Port(s) | Source/Dest | Rationale |
|------|-----------|----------|---------|-------------|-----------|
| `AllowInternetHTTPS` | Ingress | TCP | 443 | `0.0.0.0/0` | Public web access |
| `AllowBackendEgress` | Egress | TCP | 30000-32767 | Private Compute Security Group | Forward traffic to internal nodes |

### SecureWebListener
Configuration for the encrypted listener.

| Property | Value | Description |
|----------|-------|-------------|
| `Port` | 443 | Secure web port |
| `Protocol` | HTTPS | Encrypted transport |
| `SslPolicy` | TLS 1.3 | Modern encryption protocol policy |

### DestinationTargetPool
Grouping of backend endpoints.

| Property | Value | Description |
|----------|-------|-------------|
| `Protocol` | HTTP/HTTPS | Protocol for internal communication |
| `HealthCheckPath` | `/healthz` | Endpoint for availability validation |
| `HealthCheckInterval` | 15s | Frequency of health validation |

## State Transitions
1. **Unconfigured**: Initial state.
2. **Provisioning**: Pulumi creating resources (LB, Listener, Target Group, Security Rules).
3. **Active**: LB is online and accepting traffic.
4. **Degraded**: One or more backend nodes failed health checks.
5. **Locked**: Deletion protection enabled, preventing teardown.
