# Tasks: Perimeter Security Firewalls for Kubernetes Layer Isolation

**Input**: Design documents from `/specs/008-network-firewall-isolation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Mock-first unit tests are required per the project constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths follow the `infra/security/` structure defined in `plan.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create security module directory structure in infra/security/
- [ ] T002 Create empty __init__.py in infra/security/__init__.py
- [ ] T003 [P] Add perimeter security configuration properties to InfrastructureConfig in infra/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement abstract SecurityComponent base class in infra/security/base.py
- [ ] T005 Implement SecurityProviderFactory in infra/security/factory.py
- [ ] T006 [P] Register SecurityProviderFactory in infra/providers.py
- [ ] T007 Create base unit test suite for security components in tests/security/test_base.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Public Web Entry Hardening (Priority: P1) 🎯 MVP

**Goal**: Establish the safe public-facing channel accepting only HTTPS.

**Independent Test**: Send simulated web requests to public entryway; confirm only port 443 is accepted and routed to compute.

### Tests for User Story 1 (REQUIRED)

- [ ] T008 [P] [US1] Create mock unit tests for AWS Public Perimeter in tests/security/test_aws_public.py
- [ ] T009 [P] [US1] Create mock unit tests for Azure Public Perimeter in tests/security/test_azure_public.py
- [ ] T010 [P] [US1] Create mock unit tests for GCP Public Perimeter in tests/security/test_gcp_public.py

### Implementation for User Story 1

- [ ] T011 [P] [US1] Implement AWS Public Security Group (FR-002) in infra/security/aws_security.py
- [ ] T012 [P] [US1] Implement Azure Public NSG (FR-002) in infra/security/azure_security.py
- [ ] T013 [P] [US1] Implement GCP Public Firewall Rule (FR-002) in infra/security/gcp_security.py

**Checkpoint**: User Story 1 (Public Hardening) is functional and testable independently.

---

## Phase 4: User Story 2 - Compute Cluster Protection (Priority: P2)

**Goal**: Block administrative lockout (SSH) and restrict internal compute access.

**Independent Test**: Verify external SSH connection attempts are rejected; confirm internal application communication is allowed.

### Tests for User Story 2 (REQUIRED)

- [ ] T014 [P] [US2] Create mock unit tests for AWS Compute Perimeter in tests/security/test_aws_compute.py
- [ ] T015 [P] [US2] Create mock unit tests for Azure Compute Perimeter in tests/security/test_azure_compute.py
- [ ] T016 [P] [US2] Create mock unit tests for GCP Compute Perimeter in tests/security/test_gcp_compute.py

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement AWS Compute Security Group and SSH block (FR-004) in infra/security/aws_security.py
- [ ] T018 [P] [US2] Implement Azure Compute NSG and SSH block (FR-004) in infra/security/azure_security.py
- [ ] T019 [P] [US2] Implement GCP Compute Firewall Rule and SSH block (FR-004) in infra/security/gcp_security.py
- [ ] T020 [US2] Implement Domain Whitelisting for Compute Outbound (FR-007) in infra/security/ factory.py and provider files

**Checkpoint**: User Story 2 (Compute Protection) is functional and testable independently.

---

## Phase 5: User Story 3 - Data Tier Zero-Outbound Hardening (Priority: P3)

**Goal**: Protect company records against exfiltration via strict zero-outbound policy.

**Independent Test**: Verify DB only accepts connections from compute; confirm 100% failure rate for DB-initiated outbound connections.

### Tests for User Story 3 (REQUIRED)

- [ ] T021 [P] [US3] Create mock unit tests for AWS Data Perimeter in tests/security/test_aws_data.py
- [ ] T022 [P] [US3] Create mock unit tests for Azure Data Perimeter in tests/security/test_azure_data.py
- [ ] T023 [P] [US3] Create mock unit tests for GCP Data Perimeter in tests/security/test_gcp_data.py

### Implementation for User Story 3

- [ ] T024 [P] [US3] Implement AWS Data Security Group with PostgreSQL restriction (FR-005, FR-006) in infra/security/aws_security.py
- [ ] T025 [P] [US3] Implement Azure Data NSG with PostgreSQL restriction (FR-005, FR-006) in infra/security/azure_security.py
- [ ] T026 [P] [US3] Implement GCP Data Firewall Rule with PostgreSQL restriction (FR-005, FR-006) in infra/security/gcp_security.py

**Checkpoint**: User Story 3 (Data Isolation) is functional and testable independently.

---

## Phase 6: User Story 4 - Security Perimeter Lifecycle Resilience (Priority: P4)

**Goal**: Prevent accidental automated destruction of security perimeters.

**Independent Test**: Attempt deletion of perimeters while resources are live; confirm Pulumi blocks the request.

### Implementation for User Story 4

- [ ] T027 [US4] Enforce pulumi.ResourceOptions(protect=True) in SecurityComponent base class in infra/security/base.py
- [ ] T028 [US4] Implement 365-day security log retention (FR-009) in infra/security/aws_security.py
- [ ] T029 [US4] Implement 365-day security log retention (FR-009) in infra/security/azure_security.py
- [ ] T030 [US4] Implement 365-day security log retention (FR-009) in infra/security/gcp_security.py

**Checkpoint**: Lifecycle protection and 365-day logging active across all perimeters.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T031 [P] Update infra/security/README.md with multi-cloud configuration guide
- [ ] T032 Final execution of pytest suite in tests/security/
- [ ] T033 Run quickstart.md validation scenarios for all providers

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1).
- **User Stories (Phase 3-6)**: All depend on Foundational (Phase 2).
- **Polish (Phase 7)**: Depends on all user stories.

### User Story Dependencies

- **User Story 1 (P1)**: Independent.
- **User Story 2 (P2)**: Independent, can run parallel to US1.
- **User Story 3 (P3)**: Independent, can run parallel to US1/US2.
- **User Story 4 (P4)**: Independent, can run parallel to US1/US2/US3.

### Parallel Opportunities

- All AWS/Azure/GCP implementation tasks marked [P] within a story can run in parallel.
- All unit tests [P] within a story can run in parallel.
- Once Phase 2 is complete, US1, US2, and US3 implementation can proceed in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete User Story 1 (Phase 3)
4. **VALIDATE**: Run quickstart.md Scenario 1.

### Incremental Delivery

1. Foundation → Security Factory Ready.
2. User Story 1 → Public Entry Hardened.
3. User Story 2 → Compute Tier Isolated.
4. User Story 3 → Data Tier Isolated.
5. User Story 4 → Compliance and Persistence Ready.
