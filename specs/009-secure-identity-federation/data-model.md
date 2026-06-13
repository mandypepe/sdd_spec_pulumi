# Data Model: Workload Identity Federation (K8s)

## Overview
This document defines the logical entities and relationships required to establish multi-cloud identity federation for Kubernetes workloads.

## Entities

### WorkloadIdentity
Represents the cryptographic identity of an active application component.
- **Attributes**:
  - `name`: Logical identifier.
  - `namespace`: K8s namespace where the workload runs.
  - `service_account_name`: K8s Service Account associated with the workload.
  - `provider`: Target cloud provider [AWS, AZURE, GCP].
  - `federated_role_id`: The cloud-native IAM/Identity ID that the workload assumes.

### TrustRelationship
Defines the OIDC trust between the K8s cluster and the cloud provider.
- **Attributes**:
  - `oidc_issuer_url`: The URL of the cluster's OIDC discovery endpoint.
  - `thumbprint`: OIDC provider thumbprint.
  - `audience`: Expected audience for the tokens (e.g., `sts.amazonaws.com`).

### AccessScope
Defines the permissions granted to the WorkloadIdentity.
- **Attributes**:
  - `path`: Resource-specific data path (e.g., vault secret path, bucket prefix).
  - `action`: [READ_ONLY, READ_WRITE].
  - `duration`: Token TTL (60 mins).

## Relationships
- A **WorkloadIdentity** is bound to a **TrustRelationship**.
- A **WorkloadIdentity** is granted one or more **AccessScopes**.
- **TrustRelationship** is configured at the Cluster level.
