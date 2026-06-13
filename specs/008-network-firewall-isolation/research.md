# Research: Multi-Cloud Perimeter Security and Firewall Isolation

## Overview
This research document addresses the technical requirements for HU-SEC-007, focusing on implementing three-tier network isolation across AWS, Azure, and GCP using Pulumi.

## Decision: Layer-Specific Security Components
**Rationale**: To comply with FR-001 (three separate perimeters), we will implement a `PerimeterComponent` that encapsulates provider-specific firewall resources for each tier.
**Alternatives Considered**: 
- Monolithic Security Group (Rejected: Violates FR-001 isolation).
- Network ACLs (NACLs) only (Rejected: NACLs are stateless and harder to manage for fine-grained application rules; will be used as a secondary layer if needed).

## Decision: Multi-Cloud Firewall Mapping
| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Public Perimeter | Security Group (Ingress 443) | NSG (Rule 443) | FW Rule (Allow 443) |
| Compute Perimeter | Security Group (Ingress from Public) | NSG (Source ASG/NSG) | FW Rule (Target Tags) |
| Data Perimeter | Security Group (Ingress from Compute) | NSG (Source ASG/NSG) | FW Rule (Target Tags) |
| Zero-Outbound | SG Egress [] | NSG Deny Outbound | FW Rule (Deny All Egress) |

## Decision: 365-Day Log Retention
**Rationale**: Compliance requirement (FR-009).
- **AWS**: CloudWatch Log Group with `retention_in_days=365`.
- **Azure**: Storage Account with Lifecycle Management policy to transition/delete after 365 days.
- **GCP**: Cloud Logging bucket with `retention_days=365`.

## Decision: Outbound Domain Whitelisting (FR-007)
**Rationale**: Required for secure updates.
- **AWS**: Route traffic through NAT Gateway + Proxy (or FQDN filtering if available via AWS Network Firewall, but NAT Gateway + security rules is standard for MVP).
- **Azure**: Azure Firewall or NAT Gateway with Service Tags.
- **GCP**: Cloud NAT + Firewall Policies with FQDN filtering (Preview/Advanced) or Proxy.
- **Unified Approach**: Use a dedicated "Exit Gateway" pattern documented in `data-model.md`.

## Decision: Lifecycle Protection (FR-008)
**Rationale**: Prevent accidental deletion.
**Implementation**: Apply `pulumi.ResourceOptions(protect=True)` to all `PerimeterComponent` resources.

## Decision: Latency Performance (< 5ms)
**Rationale**: Cloud-native firewalls operate at the VPC/VNet SDN layer (Layer 4). They introduce negligible latency (sub-millisecond), well within the 5ms target. No specialized hardware acceleration is required.
