# Research & Discovery: Automated Three-Tier Agnostic Virtual Private Network

## Decision: Multi-Cloud Resource Mapping

We will implement a provider-agnostic interface for the VPC topology, with concrete implementations for AWS, Azure, and GCP.

### Resource Mapping Table

| Logical Resource | AWS Resource | Azure Native Resource | GCP Resource |
|------------------|--------------|-----------------------|--------------|
| VPC / Network | `aws.ec2.Vpc` | `azure_native.network.VirtualNetwork` | `gcp.compute.Network` |
| Subnet | `aws.ec2.Subnet` | `azure_native.network.Subnet` | `gcp.compute.Subnetwork` |
| Internet Gateway | `aws.ec2.InternetGateway` | Implicit / Public IP | Implicit / Routes |
| NAT Gateway | `aws.ec2.NatGateway` | `azure_native.network.NatGateway` | `gcp.compute.RouterNat` |
| VPC Flow Logs | `aws.ec2.FlowLog` | `azure_native.network.FlowLog` | `gcp.compute.Subnetwork` (log_config) |
| Security | `aws.ec2.SecurityGroup` | `azure_native.network.NetworkSecurityGroup` | `gcp.compute.Firewall` |

## Rationale

- **Pulumi Native Providers**: Using `aws`, `azure-native`, and `gcp` ensures we have the most up-to-date and comprehensive resource coverage.
- **ComponentResource Pattern**: Inheriting from `pulumi.ComponentResource` allows us to group related resources and manage them as a single logical unit, maintaining a clean state graph.
- **Strict Zone Alignment**: Implementing logic within each provider module to ensure subnets and NAT gateways are physically anchored in the same availability zone.

## Alternatives Considered

- **Pulumi Crosswalk (AWSX)**: Rejected because we need a solution that works across multiple clouds, not just AWS.
- **Terraform Modules via Pulumi**: Rejected to maintain native Python code and full leverage of Pulumi's programming model.
- **Standard Azure Provider**: Rejected in favor of `azure-native` for better alignment with project standards and API coverage.
