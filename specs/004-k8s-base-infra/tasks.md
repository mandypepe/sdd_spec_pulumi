# Tasks: K8s Base Infrastructure

**Input**: Design documents from `/specs/004-k8s-base-infra/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [X] T001 Create orchestrator infrastructure structure in infra/orchestrator/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Add K8s infrastructure configuration fields to infra/config.py
- [X] T003 Define K8s infrastructure constants in infra/constants.py
- [X] T004 Implement OrchestratorProviderFactory in infra/orchestrator/base.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Multi-AZ Orchestrator Layer Provisioning (Priority: P1) 🎯 MVP

**Goal**: Provision the K8s orchestrator control plane and compute nodes across two isolated availability zones.

**Independent Test**: Verify orchestrator control plane and compute nodes initialize in distinct subnets with no public IPs.

### Implementation for User Story 1

- [X] T005 [P] Implement base OrchestratorComponent in infra/orchestrator/base.py
- [X] T006 [P] Implement AwsK8sComponent in infra/orchestrator/aws_k8s.py
- [X] T007 [P] Implement AzureK8sComponent in infra/orchestrator/azure_k8s.py
- [X] T008 [P] Implement GcpK8sComponent in infra/orchestrator/gcp_k8s.py
- [X] T009 [US1] Register providers in OrchestratorProviderFactory in infra/orchestrator/base.py

**Checkpoint**: User Story 1 functional

---

## Phase 4: User Story 2 - Perimeter Traffic Control (Priority: P2)

**Goal**: Enforce perimeter security, blocking administrative traffic and restricting outbound traffic.

**Independent Test**: Scan for admin ports and verify all connections drop; verify outbound traffic routes through translation gateways.

### Implementation for User Story 2

- [X] T010 [P] [US2] Implement security firewall rules for AWS in infra/orchestrator/aws_k8s.py
- [X] T011 [P] [US2] Implement security firewall rules for Azure in infra/orchestrator/azure_k8s.py
- [X] T012 [P] [US2] Implement security firewall rules for GCP in infra/orchestrator/gcp_k8s.py

**Checkpoint**: User Story 2 functional

---

## Phase 5: User Story 3 - Federated Identity (Priority: P3)

**Goal**: Integrate passwordless token-based authentication.

**Independent Test**: Query authentication subsystem and verify federated token usage.

### Implementation for User Story 3

- [X] T013 [P] [US3] Implement federated identity setup for AWS in infra/orchestrator/aws_k8s.py
- [X] T014 [P] [US3] Implement federated identity setup for Azure in infra/orchestrator/azure_k8s.py
- [X] T015 [P] [US3] Implement federated identity setup for GCP in infra/orchestrator/gcp_k8s.py

**Checkpoint**: User Story 3 functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validation

- [X] T016 [P] Add unit tests for AWS K8s component in tests/orchestrator/test_aws_k8s.py
- [X] T017 [P] Add unit tests for factory in tests/orchestrator/test_factory.py
- [X] T018 Run quickstart.md validation scenarios
- [X] T019 Final documentation review

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Stories (Phase 3-5)**: All depend on Foundational completion.
- **Polish (Phase 6)**: Depends on all user stories.

### Parallel Opportunities

- Provider implementations (T006-T008, T010-T012, T013-T015) can run in parallel for different clouds.
- Polish tasks (T016-T017) can run in parallel.
