# Tasks: Provisioning of a Managed Database in an Isolated Layer

**Input**: Design documents from `/specs/007-branchname-feature-hu/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Mock-based unit tests are REQUIRED as per the constitution (Principle V) and the project guidelines.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure for `infra/db/` and `tests/db/` per implementation plan
- [X] T002 Initialize `infra/db/__init__.py` and `tests/db/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Define `DatabaseOutputs` typed metadata in `infra/db/base.py`
- [X] T004 Implement abstract `DatabaseComponent` base class in `infra/db/base.py` (incorporating `contracts/database_component.md`)
- [X] T005 [P] Update `InfrastructureConfig` in `infra/config.py` to include managed database settings (engine, instance class, storage, etc.)
- [X] T006 Implement `DatabaseProviderFactory` in `infra/providers.py` to handle "aws", "azure", and "gcp" types
- [X] T007 [P] Create mock infrastructure helpers for database tests in `tests/db/conftest.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Complete Network Segregation (Priority: P1) 🎯 MVP

**Goal**: Ensure database subnets are fully isolated from the public internet.

**Independent Test**: `tests/db/test_network_isolation.py` confirms routing tables for DB subnets do not contain `0.0.0.0/0`.

### Tests for User Story 1

- [X] T008 [P] [US1] Create network isolation validation test in `tests/db/test_network_isolation.py`

### Implementation for User Story 1

- [X] T009 [US1] Implement `configure_network` logic in `infra/db/aws_db.py` to ensure zero public routes
- [X] T010 [US1] Implement `configure_network` logic in `infra/db/azure_db.py` to ensure zero public routes
- [X] T011 [US1] Implement `configure_network` logic in `infra/db/gcp_db.py` to ensure zero public routes

**Checkpoint**: At this point, network isolation logic for all providers is functional and testable.

---

## Phase 4: User Story 2 - High Availability and Geographic Resiliency (Priority: P1)

**Goal**: Provision a database cluster distributed across multiple availability zones.

**Independent Test**: `tests/db/test_factory.py` verifies instances are distributed across 2+ zones.

### Tests for User Story 2

- [X] T012 [P] [US2] Create multi-zone distribution test in `tests/db/test_factory.py`

### Implementation for User Story 2

- [X] T013 [US2] Implement `provision` logic in `infra/db/aws_db.py` for Multi-AZ RDS/Aurora
- [X] T014 [US2] Implement `provision` logic in `infra/db/azure_db.py` for Zone-redundant Flexible Server
- [X] T015 [US2] Implement `provision` logic in `infra/db/gcp_db.py` for Regional Cloud SQL

**Checkpoint**: Multi-zone provisioning is functional across all providers.

---

## Phase 5: User Story 3 - Role-Based Boundary Access Control (Priority: P1)

**Goal**: Restrict ingress to authorized compute nodes and deny all egress traffic.

**Independent Test**: `tests/db/test_security_rules.py` verifies firewall rules allow only specific port/source pairs.

### Tests for User Story 3

- [X] T016 [P] [US3] Create perimeter security validation tests in `tests/db/test_security_rules.py`

### Implementation for User Story 3

- [X] T017 [US3] Implement `configure_security` in `infra/db/aws_db.py` (Security Groups)
- [X] T018 [US3] Implement `configure_security` in `infra/db/azure_db.py` (Firewall Rules/NSG)
- [X] T019 [US3] Implement `configure_security` in `infra/db/gcp_db.py` (Firewall Rules)

**Checkpoint**: Perimeter access control is enforced for all providers.

---

## Phase 6: User Story 4 - Infrastructure Destruction Protection (Priority: P2)

**Goal**: Prevent accidental deletion using lifecycle protection rules.

**Independent Test**: `tests/db/test_deletion_protection.py` verifies `deletion_protection=True` or equivalent lifecycle options.

### Tests for User Story 4

- [X] T020 [P] [US4] Create deletion protection validation tests in `tests/db/test_deletion_protection.py`

### Implementation for User Story 4

- [X] T021 [US4] Add `deletion_protection=True` and lifecycle hooks to `infra/db/aws_db.py`
- [X] T022 [US4] Add resource locks or protection flags to `infra/db/azure_db.py`
- [X] T023 [US4] Add `deletion_protection=True` to `infra/db/gcp_db.py`

**Checkpoint**: Persistence resources are protected against accidental deletion.

---

## Phase 7: User Story 5 - Secure Parameter Extraction (Priority: P2)

**Goal**: Export sensitive connection data as Pulumi secret outputs.

**Independent Test**: `tests/db/test_encryption.py` (or similar) verifies outputs are marked as secrets.

### Tests for User Story 5

- [X] T024 [P] [US5] Create secret output validation tests in `tests/db/test_encryption.py`

### Implementation for User Story 5

- [X] T025 [US5] Ensure all sensitive `DatabaseOutputs` in `infra/db/aws_db.py` use `pulumi.Output.secret()`
- [X] T026 [US5] Ensure all sensitive `DatabaseOutputs` in `infra/db/azure_db.py` use `pulumi.Output.secret()`
- [X] T027 [US5] Ensure all sensitive `DatabaseOutputs` in `infra/db/gcp_db.py` use `pulumi.Output.secret()`

**Checkpoint**: Connection metadata is securely handled.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [X] T028 Update `README.md` with Managed Database component usage examples
- [X] T029 [P] Run all tests across the project: `pytest tests/db/`
- [X] T030 Run `quickstart.md` validation scenarios end-to-end (mocks)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on T001, T002. BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Phase 2 completion.
- **Polish (Phase 8)**: Depends on completion of all P1/P2 user stories.

### Parallel Opportunities

- T005, T007 (Foundational) can run in parallel.
- Test tasks for different stories (T008, T012, T016, T020, T024) can run in parallel once Foundation is ready.
- Implementation of different providers (AWS, Azure, GCP) within the same story can run in parallel if multiple developers are available.

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3)

1. Complete Setup + Foundational.
2. Complete US1 (Isolation), US2 (HA), and US3 (Security) for at least one provider (e.g., AWS).
3. **STOP and VALIDATE**: Test primary functionality using `pytest`.

### Parallel Team Strategy

- Dev A: AWS implementation across all stories.
- Dev B: Azure implementation across all stories.
- Dev C: GCP implementation across all stories.
- All devs collaborate on Foundational/Base classes.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label for traceability.
- All sensitive outputs MUST be wrapped in `pulumi.Output.secret()`.
- Deletion protection is mandatory for all persistence resources.
