# Quickstart: Validating the Managed Database Component

## Prerequisites

- Python 3.11+
- Pulumi CLI
- Virtual environment with dependencies installed (`pip install -r requirements.txt`)

## Setup

```bash
# Set up environment
$env:PYTHONPATH = "."
```

## Validation Scenarios

### 1. Network Isolation Test
Verify that the database subnets have no internet access.

```bash
# Run mock-based tests
pytest tests/db/test_network_isolation.py -v
```
**Expected**: Test confirms routing tables for DB subnets do not contain `0.0.0.0/0`.

### 2. High Availability Test
Verify that the cluster is distributed across multiple zones.

```bash
pytest tests/db/test_factory.py -v
```
**Expected**: Mock output shows instances in at least 2 distinct availability zones.

### 3. Deletion Protection Test
Verify that the `deletion_protection` or lifecycle rules are active.

```bash
pytest tests/db/test_aws_db.py -k "test_deletion_protection" -v
```
**Expected**: Mock resource definition includes `deletion_protection=True`.

### 4. Encryption Test
Verify AES-256 encryption-at-rest.

```bash
pytest tests/db/test_encryption.py -v
```
**Expected**: Mock output shows `storage_encrypted=True` or provider-equivalent.

## Cleanup

No physical cleanup required if using mocks. If deployed to a real stack, remember to manually disable `deletion_protection` before `pulumi destroy` if removal is intended.
