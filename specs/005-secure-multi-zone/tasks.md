# Tasks: Secure Multi-Zone Automated Compute Data Plane

**Input**: Design documents from `specs/005-secure-multi-zone/`

**Prerequisites**: plan.md, spec.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup

- [ ] T001 [P] Define `OrchestratorConfig` in `infra/config.py`
- [ ] T002 [P] Implement `OrchestratorComponent` base interface in `infra/orchestrator/base.py`
- [ ] T003 [P] Implement `OrchestratorProviderFactory` in `infra/orchestrator/__init__.py`

## Phase 2: Foundational

- [ ] T004 [P] Setup mock-based test suite in `tests/orchestrator/test_factory.py`

---

## Phase 3: User Story 1 - Multi-Zone Private Network Isolation (Priority: P1) 🎯 MVP

**Goal**: Establish isolated, multi-zone compute data plane across private subnets.

- [ ] T005 [P] [US1] Implement `AwsK8sComponent` with multi-zone subnet logic in `infra/orchestrator/aws_k8s.py`
- [ ] T006 [P] [US1] Implement `AzureK8sComponent` with multi-zone subnet logic in `infra/orchestrator/azure_k8s.py`
- [ ] T007 [P] [US1] Implement `GcpK8sComponent` with multi-zone subnet logic in `infra/orchestrator/gcp_k8s.py`
- [ ] T008 [TDD] [US1] Add unit tests for multi-zone subnet assignment in `tests/orchestrator/test_aws_k8s.py`
- [ ] T009 [TDD] [US1] Add unit tests for multi-zone subnet assignment in `tests/orchestrator/test_azure_k8s.py`
- [ ] T010 [TDD] [US1] Add unit tests for multi-zone subnet assignment in `tests/orchestrator/test_gcp_k8s.py`

**Checkpoint**: Multi-zone isolation confirmed via mock-based tests.

---

## Phase 4: User Story 2 - Automated Scaling Synchronization and Idempotence (Priority: P2)

**Goal**: Ensure infrastructure automation does not disrupt active scaling operations.

- [ ] T011 [US2] Enhance `OrchestratorComponent` to support state-preservation during scaling in `infra/orchestrator/base.py`
- [ ] T012 [US2] Update provider components (`aws_k8s`, `azure_k8s`, `gcp_k8s`) to implement resource state preservation logic in `infra/orchestrator/`
- [ ] T013 [TDD] [US2] Add unit tests verifying scaling synchronization in `tests/orchestrator/test_factory.py`

**Checkpoint**: Infrastructure blueprint updates demonstrate idempotency for scaling nodes.

---

## Phase 5: User Story 3 - Restricted Perimeter Enforcement & Access Rejection (Priority: P3)

**Goal**: Enforce strict network perimeter boundaries.

- [ ] T014 [US3] Implement perimeter firewall/security group rules in `infra/orchestrator/base.py`
- [ ] T015 [US3] Update provider components to restrict outbound traffic to authorized proxies/databases in `infra/orchestrator/`
- [ ] T016 [TDD] [US3] Add unit tests for perimeter rule verification in `tests/orchestrator/test_factory.py`

**Checkpoint**: Perimeter enforcement rules confirm unauthorized traffic is blocked.

---

## Phase 6: User Story 4 - Minimum Privilege Identity Governance (Priority: P4)

**Goal**: Enforce least-privilege host identities.

- [ ] T017 [US4] Define restricted IAM roles/service accounts for orchestrator compute nodes in `infra/orchestrator/base.py`
- [ ] T018 [US4] Update provider components to attach restricted identity to compute hosts in `infra/orchestrator/`
- [ ] T019 [TDD] [US4] Add unit tests for host identity privilege audit in `tests/orchestrator/test_factory.py`

**Checkpoint**: Host identity privilege audit succeeds.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T020 [P] Documentation update for new orchestrator capabilities in `README.md`
- [ ] T021 [P] Code cleanup and refactoring of `OrchestratorComponent`
- [ ] T022 [P] Final compliance audit of all implemented infrastructure logic
