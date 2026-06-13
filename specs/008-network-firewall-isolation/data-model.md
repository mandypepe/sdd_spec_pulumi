# Data Model: Perimeter Security and Firewall Isolation

## Overview
This document defines the logical entities and relationships used to implement the multi-cloud perimeter security framework.

## Entities

### SecurityPerimeter
Represents a hardened network boundary for a specific infrastructure tier.
- **Attributes**:
  - `name`: Logical identifier (e.g., "public", "compute", "data").
  - `tier`: One of [PUBLIC, PRIVATE, ISOLATED].
  - `provider`: Target cloud provider [AWS, AZURE, GCP].
  - `resource_id`: Native ID of the firewall resource (SG ID, NSG Name, etc.).
  - `is_protected`: Boolean (True enforces FR-008).

### AccessRule
Defines a specific traffic flow allowed or denied through a perimeter.
- **Attributes**:
  - `direction`: [INBOUND, OUTBOUND].
  - `protocol`: [TCP, UDP, ICMP, ALL].
  - `port_range`: Specific ports or ranges.
  - `source_destination`: CIDR block, Security Group ID, or Service Tag.
  - `action`: [ALLOW, DENY].

### AuditLogConfiguration
Configuration for security event logging and retention.
- **Attributes**:
  - `retention_days`: Fixed at 365 (FR-009).
  - `format`: W3C Extended Log Format.
  - `destination`: Cloud-native logging sink (Log Group, Storage Bucket, etc.).

## Relationships
- A **SecurityPerimeter** contains multiple **AccessRules**.
- Each **SecurityPerimeter** is associated with an **AuditLogConfiguration**.
- **Perimeters** are linked to **Subnets** defined in the `VpcComponent`.

## State Transitions
1. **Provisioned**: Perimeter and initial rules created.
2. **Hardened**: All Default-Deny rules applied and verified.
3. **Protected**: Lifecycle destruction lock active (`protect=True`).
4. **Audited**: Flow logs active and reaching the 365-day retention sink.
