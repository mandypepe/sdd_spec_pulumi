# Quickstart: Secure Container Registry Validation

## Overview
This document outlines runnable validation scenarios to confirm the Secure Container Registry feature functions correctly end-to-end.

## Prerequisites
- Authenticated environment (AWS/Azure/GCP).
- Pulumi CLI installed.
- Access to enterprise KMS (or mock key).

## Setup
1. Define registry configuration in `infra/config.py`.
2. Run `pulumi up` to provision the `SecureRegistry` component.

## Validation Scenarios

### Scenario 1: Private Access Verification
- **Action**: Attempt to `docker pull` or `list` repository contents from an unauthenticated environment.
- **Expected Outcome**: Connection rejected (403 Forbidden/Unauthorized).

### Scenario 2: Tag Immutability Test
- **Action**: 
    1. Push an image with tag `v1.0.0`.
    2. Attempt to push a different image with the same tag `v1.0.0`.
- **Expected Outcome**: Push rejected by the registry.

### Scenario 3: Automated Scan Trigger
- **Action**: Push a new image to the repository.
- **Expected Outcome**: Vulnerability scanning status updates to "In Progress" or "Complete" within 5 seconds.

## References
- Data Model: [data-model.md](data-model.md)
- Contracts: [contracts/](contracts/)
