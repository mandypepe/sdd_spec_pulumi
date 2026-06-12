# Tasks: Public Multi-Zone Traffic Routing and Perimeter Security Policy

**Input**: Design documents from `specs/003-external-lb-security/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/lb_component.md](contracts/lb_component.md)

**Tests**: Included as per "Mock-First Unit Testing" principle in [constitution.md](../../.specify/memory/constitution.md).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `infra/lb/` directory and `infra/lb/__init__.py`
- [X] T002 Create `tests/lb/` directory and `tests/lb/conftest.py`
- [X] T003 Configure `tests/conftest.py` to include any shared LB mocks

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T004 Define `LbComponent` base class in `infra/lb/base.py`
- [X] T005 Implement `LbProviderFactory` in `infra/providers.py`
- [X] T006 [P] Create factory unit tests in `tests/lb/test_factory.py`
- [X] T007 Define `LbConfig` schema in `infra/config.py`

---

## Phase 3: User Story 1 - Secure High-Availability Entry Point Delivery (Priority: P1) 🎯 MVP

**Goal**: Automatically deploy a public-facing entry point across multiple isolated availability zones.

**Independent Test**: Verify that a public-facing traffic management system is constructed and bound exclusively to the designated public network sectors.

### Tests for User Story 1

- [X] T008 [P] [US1] Create mock-first unit test for AWS ALB creation in `tests/lb/test_aws_lb.py`
- [X] T009 [P] [US1] Create mock-first unit test for Azure AppGW creation in `tests/lb/test_azure_lb.py`
- [X] T010 [P] [US1] Create mock-first unit test for GCP LB creation in `tests/lb/test_gcp_lb.py`

### Implementation for User Story 1

- [X] T011 [US1] Implement basic AWS ALB with multi-zone subnet support in `infra/lb/aws_lb.py`
- [X] T012 [US1] Implement basic Azure AppGW with multi-zone subnet support in `infra/lb/azure_lb.py`
- [X] T013 [US1] Implement basic GCP LB with multi-zone subnet support in `infra/lb/gcp_lb.py`

---

## Phase 4: User Story 2 - Encrypted Traffic Interception and Target Redirection (Priority: P2)

**Goal**: Accept only high-grade encrypted web connections and securely route requests to internal nodes.

**Independent Test**: Confirm that unencrypted requests are dropped and encrypted requests are forwarded to the internal application range.

### Tests for User Story 2

- [X] T014 [P] [US2] Update unit tests in `tests/lb/test_aws_lb.py` to verify TLS 1.3 and port forwarding
- [X] T015 [P] [US2] Update unit tests in `tests/lb/test_azure_lb.py` to verify TLS 1.3 and port forwarding
- [X] T016 [P] [US2] Update unit tests in `tests/lb/test_gcp_lb.py` to verify TLS 1.3 and port forwarding

### Implementation for User Story 2

- [X] T017 [US2] Configure TLS 1.3 listener and backend target group in `infra/lb/aws_lb.py`
- [X] T018 [US2] Configure TLS 1.3 listener and backend settings in `infra/lb/azure_lb.py`
- [X] T019 [US2] Configure TLS 1.3 listener and backend service in `infra/lb/gcp_lb.py`

---

## Phase 5: User Story 3 - Continuous Target Health Monitoring (Priority: P3)

**Goal**: Continuously evaluate the operational availability of internal execution nodes.

**Independent Test**: Verify that unhealthy nodes are removed from service within 15 seconds.

### Tests for User Story 3

- [X] T020 [P] [US3] Update unit tests in `tests/lb/test_aws_lb.py` to verify 15s health check interval
- [X] T021 [P] [US3] Update unit tests in `tests/lb/test_azure_lb.py` to verify 15s health check interval
- [X] T022 [P] [US3] Update unit tests in `tests/lb/test_gcp_lb.py` to verify 15s health check interval

### Implementation for User Story 3

- [X] T023 [US3] Implement 15s health check configuration for AWS in `infra/lb/aws_lb.py`
- [X] T024 [US3] Implement 15s health check configuration for Azure in `infra/lb/azure_lb.py`
- [X] T025 [US3] Implement 15s health check configuration for GCP in `infra/lb/gcp_lb.py`

---

## Phase 6: User Story 4 - Structural Infrastructure Decommissioning Safeguards (Priority: P4)

**Goal**: Prevent accidental asset deletion during production updates or concurrent execution runs.

**Independent Test**: Verify that destruction commands are rejected by the orchestration engine.

### Tests for User Story 4

- [X] T026 [P] [US4] Update unit tests in `tests/lb/test_aws_lb.py` to verify deletion protection
- [X] T027 [P] [US4] Update unit tests in `tests/lb/test_azure_lb.py` to verify resource locks
- [X] T028 [P] [US4] Update unit tests in `tests/lb/test_gcp_lb.py` to verify deletion protection

### Implementation for User Story 4

- [X] T029 [US4] Implement `enable_deletion_protection` and `protect=True` in `infra/lb/aws_lb.py`
- [X] T030 [US4] Implement `ManagementLock` and `protect=True` in `infra/lb/azure_lb.py`
- [X] T031 [US4] Implement `delete_protection` and `protect=True` in `infra/lb/gcp_lb.py`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and clean-up

- [X] T032 [P] Export `LbProviderFactory` in `infra/__init__.py`
- [X] T033 Run all unit tests in `tests/lb/` and verify pass rate
- [X] T034 Perform manual validation using `quickstart.md` scenarios
- [X] T035 [P] Update root `README.md` with new LB module capabilities

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Stories (Phase 3-6)**: All depend on Phase 2 completion.
- **Polish (Phase 7)**: Depends on all user stories being complete.

### Parallel Opportunities

- Provider-specific implementation tasks (AWS, Azure, GCP) can run in parallel within each story phase.
- Unit tests for different providers can run in parallel.
- Foundational setup tasks (T006, T007) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Implement User Story 1 (Basic LB deployment across multiple zones).
3. Validate with `pytest tests/lb/`.

### Incremental Delivery

1. Foundation -> Ready for development.
2. User Story 1 -> Multi-zone entry point (P1).
3. User Story 2 -> Security & TLS 1.3 (P2).
4. User Story 3 -> High availability & Health checks (P3).
5. User Story 4 -> Operational safety (P4).
