# Data Model: Automated Three-Tier Agnostic Virtual Private Network

## Entities

### VpcComponent (Abstract)

Base class for all provider-specific VPC implementations.

- **Attributes**:
    - `vpc_id`: Output[str] - The ID of the created VPC/Virtual Network.
    - `public_subnet_ids`: Output[list[str]] - List of public subnet IDs.
    - `private_subnet_ids`: Output[list[str]] - List of private subnet IDs.
    - `isolated_subnet_ids`: Output[list[str]] - List of isolated subnet IDs.
- **Relationships**:
    - Contains 6 `NetworkSubnet` resources.
    - Contains 2 `NatGateway` resources (pinned to zones).
    - Contains 1 `InternetGateway` resource.

### NetworkSubnet

Represents a slice of the VPC address space.

- **Attributes**:
    - `name`: str - Unique identifier (e.g., `public-subnet-1`).
    - `cidr_block`: str - IPv4 address range (e.g., `10.0.1.0/24`).
    - `availability_zone`: str - Physical zone assignment.
    - `tier`: enum - `PUBLIC`, `PRIVATE`, or `ISOLATED`.
- **Validation Rules**:
    - `cidr_block` must be within the `VpcComponent` CIDR range.
    - `availability_zone` must be one of the two targeted zones.

### SecurityPolicy (Firewall)

Defines traffic rules for a tier.

- **Attributes**:
    - `ingress_rules`: list[Rule] - Allowed inbound traffic.
    - `egress_rules`: list[Rule] - Allowed outbound traffic.
- **State Transitions**:
    - Rules are immutable after creation within a stack run.

## Validation Logic

- **CIDR Non-Overlap**: The system must validate that all 6 subnets have non-overlapping CIDR blocks before resource creation.
- **Zone Pining**: The system must ensure that the NAT Gateway in Zone 1 is only used by private subnets in Zone 1.
