# Tasks: Secure Container Registry

**Input**: Design documents from `specs/006-secure-container-registry/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD approach using Pulumi mocks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

- [X] T001 Create project structure per implementation plan
- [X] T002 Configure registry component factory in infra/orchestrator/

---

## Phase 2: Foundational

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T003 [P] Implement RegistryComponent base class in infra/registry/base.py
- [X] T004 [P] Implement RegistryProviderFactory in infra/registry/
- [X] T005 [P] Setup Pulumi mock tests in tests/registry/conftest.py
- [X] T006 [P] Add InfrastructureConfig parameters for Registry in infra/config.py

---

## Phase 3: User Story 1 - Secure and Isolated Asset Storage (Priority: P1) 🎯 MVP

**Goal**: Provision a private, encrypted container registry that denies anonymous access.

**Independent Test**: Execute provisioning and verify 403 Forbidden for anonymous requests.

- [X] T007 [P] [US1] Implement AwsRegistryComponent in infra/registry/aws_registry.py
- [X] T008 [P] [US1] Implement AzureRegistryComponent in infra/registry/azure_registry.py
- [X] T009 [P] [US1] Implement GcpRegistryComponent in infra/registry/gcp_registry.py
- [X] T010 [US1] Update ProviderFactory to support registry components
- [X] T011 [US1] Implement unit tests for US1 in tests/registry/

---

## Phase 4: User Story 2 - Image Content Protection and Immutability (Priority: P2)

**Goal**: Prevent overwriting of published software version tags.

**Independent Test**: Attempt to publish a new asset with an existing tag and confirm rejection.

- [X] T012 [US2] Update RegistryComponent base to include tag_immutability property
- [X] T013 [US2] Implement tag immutability config for AWS in infra/registry/aws_registry.py
- [X] T014 [US2] Implement tag immutability config for Azure in infra/registry/azure_registry.py
- [X] T015 [US2] Implement tag immutability config for GCP in infra/registry/gcp_registry.py
- [X] T016 [US2] Add unit tests for immutability in tests/registry/

---

## Phase 5: User Story 3 - Automated Vulnerability Assessment (Priority: P3)

**Goal**: Automatically scan assets for vulnerabilities upon upload.

**Independent Test**: Upload an asset and verify scan trigger.

- [X] T017 [US3] Update RegistryComponent base to include vulnerability_scanning property
- [X] T018 [US3] Implement scanning config for AWS in infra/registry/aws_registry.py
- [X] T019 [US3] Implement scanning config for Azure in infra/registry/azure_registry.py
- [X] T020 [US3] Implement scanning config for GCP in infra/registry/gcp_registry.py
- [X] T021 [US3] Add unit tests for scanning in tests/registry/

---

## Phase 6: User Story 4 - Identity-Based Access Control Matrix (Priority: P4)

**Goal**: Enforce least privilege access for hosting environments and delivery lines.

**Independent Test**: Authenticate and verify Read/Write permissions based on identity.

- [X] T022 [US4] Implement AccessControlPolicy component in infra/registry/
- [X] T023 [US4] Apply policy to AWS registry in infra/registry/aws_registry.py
- [X] T024 [US4] Apply policy to Azure registry in infra/registry/azure_registry.py
- [X] T025 [US4] Apply policy to GCP registry in infra/registry/gcp_registry.py
- [X] T026 [US4] Add unit tests for access policy in tests/registry/

---

## Phase 7: User Story 5 - Automatic Resource Optimization & Lifecycle Management (Priority: P5)

**Goal**: Expire untagged or redundant software packages.

**Independent Test**: Populate redundant assets and verify automated cleanup.

- [X] T027 [US5] Implement LifecycleRule component in infra/registry/
- [X] T028 [US5] Apply lifecycle rules to AWS registry in infra/registry/aws_registry.py
- [X] T029 [US5] Apply lifecycle rules to Azure registry in infra/registry/azure_registry.py
- [X] T030 [US5] Apply lifecycle rules to GCP registry in infra/registry/gcp_registry.py
- [X] T031 [US5] Add unit tests for lifecycle in tests/registry/

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T032 [P] Documentation updates in specs/006-secure-container-registry/quickstart.md
- [X] T033 Code cleanup and refactoring across infra/registry/
- [X] T034 Security hardening and peer review
- [X] T035 Run end-to-end validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Initial start
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all stories
- **Phase 3-7 (Stories)**: Depend on Phase 2
- **Phase 8 (Polish)**: Depends on completion of stories

### User Story Dependencies

- **US1 (P1)**: Independent
- **US2 (P2)**: Independent
- **US3 (P3)**: Independent
- **US4 (P4)**: Independent
- **US5 (P5)**: Independent

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2
2. Complete Phase 3 (User Story 1)
3. **VALIDATE**
4. Deploy

### Incremental Delivery

1. Setup + Foundational
2. US1 -> US2 -> US3 -> US4 -> US5
