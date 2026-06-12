# Research: Public Multi-Zone Traffic Routing and Perimeter Security Policy

## Multi-Cloud Load Balancer Implementation

### AWS (Application Load Balancer)
- **SDK**: `pulumi_aws.lb`
- **Resource**: `LoadBalancer` (type: "application"), `TargetGroup`, `Listener`.
- **TLS 1.3**: Use `ssl_policy="ELBSecurityPolicy-TLS13-1-2-Res-2021-06"`.
- **Health Check**: Set `interval=15` in `TargetGroup.health_check`.
- **Perimeter Security**: `SecurityGroup` attached to the ALB.
  - Ingress: Port 443 from `0.0.0.0/0`.
  - Egress: Port range 30000-32767 to the private compute layer security group.
- **Protection**: Set `enable_deletion_protection=True` in `LoadBalancer` and use `pulumi.ResourceOptions(protect=True)`.

### Azure (Application Gateway)
- **SDK**: `pulumi_azure_native.network`
- **Resource**: `ApplicationGateway`.
- **TLS 1.3**: Use `Standard_v2` SKU with `ssl_policy` type `CustomV2` and `min_protocol_version="TLSv1_3"`.
- **Health Probe**: Set `interval=15` in `ApplicationGatewayProbeArgs`.
- **Perimeter Security**: `NetworkSecurityGroup` (NSG) associated with the Application Gateway subnet.
  - Ingress: Port 443 from `0.0.0.0/0`.
  - Egress: Port range 30000-32767 to the backend subnet.
- **Protection**: Use `pulumi_azure_native.authorization.ManagementLockAtResourceLevel` with level `CanNotDelete` and `pulumi.ResourceOptions(protect=True)`.

### GCP (External HTTP(S) Load Balancer)
- **SDK**: `pulumi_gcp.compute`
- **Resource**: `GlobalForwardingRule`, `TargetHttpsProxy`, `URLMap`, `BackendService`, `HealthCheck`, `SSLPolicy`.
- **TLS 1.3**: `SSLPolicy` with `min_tls_version="TLS_1_2"`, `profile="MODERN"`, and `tls_early_data="ENABLED"`. Note: GCP negotiates TLS 1.3 when `min_tls_version` is 1.2 and profile is modern.
- **Health Check**: Set `check_interval_sec=15` in `HealthCheck`.
- **Perimeter Security**: `Firewall` rules in the VPC.
  - Ingress: Port 443 from `0.0.0.0/0`.
  - Egress: Port range 30000-32767 to backend instances.
- **Protection**: Set `delete_protection=True` in `GlobalForwardingRule` and use `pulumi.ResourceOptions(protect=True)`.

## Deletion Protection Strategy
We will implement a dual-layer protection strategy:
1. **Provider-Specific Flags**: Use `enable_deletion_protection` (AWS), `ManagementLock` (Azure), and `delete_protection` (GCP) to leverage cloud-native safeguards.
2. **Pulumi Lifecycle**: Use `pulumi.ResourceOptions(protect=True)` for all primary traffic manager resources to prevent Pulumi from deleting them during `pulumi up` or `pulumi destroy`.

## Security Perimeter Design
A unified security perimeter will be established across all providers:
- **External Ingress**: Strictly limited to TCP/443.
- **Internal Egress**: Strictly limited to TCP/30000-32767 toward the compute layer.
- **Protocol Enforce**: TLS 1.3 will be the preferred/minimum protocol version where supported natively.

## Decision Summary
- **Decision**: Implement a new `infra/lb` module following the existing `ComponentResource` and `Factory` patterns.
- **Rationale**: Maintains architectural consistency and supports multi-cloud requirements while providing a clean abstraction for the load balancer component.
- **Alternatives considered**: Using higher-level Pulumi Crosswalk components (e.g., `awsx`), but rejected to maintain fine-grained control and cross-provider consistency.
