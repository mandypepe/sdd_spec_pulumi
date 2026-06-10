# Tasks: Automated Three-Tier Agnostic Virtual Private Network

**Input**: Design documents from `specs/002-agnostic-vpc-topology/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested for this feature, but verification steps are included for each story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create VPC component directory structure in `infra/vpc/`
- [X] T002 Create `infra/vpc/__init__.py` and define base exports
- [X] T003 [P] Add required CIDR constants for the three-tier topology to `infra/constants.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Define abstract `VpcComponent` class in `infra/vpc/base.py`
- [X] T005 [P] Add VPC configuration parameters to `InfrastructureConfig` in `infra/config.py`
- [X] T006 Implement basic VPC instantiation logic in `infra/vpc/aws_vpc.py` (AWS boilerplate)
- [X] T007 Implement basic VPC instantiation logic in `infra/vpc/azure_vpc.py` (Azure boilerplate)
- [X] T008 Implement basic VPC instantiation logic in `infra/vpc/gcp_vpc.py` (GCP boilerplate)
- [X] T009 Register VPC components in `VpnProviderFactory` within `infra/providers.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Multi-Zone Core Isolation and Subnetting (Priority: P1) 🎯 MVP

**Goal**: Automatically provision a master virtual private network partitioned into six distinct subnets across two isolated availability zones.

**Independent Test**: Verify via `pulumi preview` that 1 VPC and 6 subnets (2 Public, 2 Private, 2 Isolated) are planned across 2 zones.

### Implementation for User Story 1

- [X] T010 [US1] Implement AWS Subnet allocation logic in `infra/vpc/aws_vpc.py`
- [X] T011 [US1] Implement Azure Virtual Network and Subnet allocation logic in `infra/vpc/azure_vpc.py`
- [X] T012 [US1] Implement GCP Network and Subnetwork allocation logic in `infra/vpc/gcp_vpc.py`
- [X] T013 [US1] Add bilingual docstrings for subnet creation methods in all `infra/vpc/*.py` files
- [X] T014 [US1] Verify subnet CIDR non-overlap validation in `infra/vpc/base.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Outbound Routing and Perimeter Gateways (Priority: P2)

**Goal**: Deploy network boundaries and physical translation mechanisms (Internet Gateway, NAT Gateways) for outbound traffic.

**Independent Test**: Verify routing tables in `pulumi preview` show public subnets pointing to IGW and private subnets pointing to zone-aligned NAT Gateways.

### Implementation for User Story 2

- [X] T015 [US2] Implement IGW and NAT Gateway creation for AWS in `infra/vpc/aws_vpc.py`
- [X] T016 [US2] Implement NAT Gateway and routing for Azure in `infra/vpc/azure_vpc.py`
- [X] T017 [US2] Implement Cloud Router and NAT for GCP in `infra/vpc/gcp_vpc.py`
- [X] T018 [US2] Configure zone-aligned routing rules in `infra/vpc/aws_vpc.py` (Strict Zone Alignment)
- [X] T019 [US2] Configure zone-aligned routing rules in `infra/vpc/azure_vpc.py` (Strict Zone Alignment)
- [X] T020 [US2] Configure zone-aligned routing rules in `infra/vpc/gcp_vpc.py` (Strict Zone Alignment)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Security Barrier Policies and Perimeter Firewalls (Priority: P3)

**Goal**: Enforce strict network-level firewall rules and filtering barriers over each individual subnet layer.

**Independent Test**: Verify firewall rules in `pulumi preview` show port 443 allowed to LB, port 5432 allowed to DB only from compute.

### Implementation for User Story 3

- [X] T021 [US3] Implement Security Group rules for AWS in `infra/vpc/aws_vpc.py`
- [X] T022 [US3] Implement Network Security Group rules for Azure in `infra/vpc/azure_vpc.py`
- [X] T023 [US3] Implement Firewall rules for GCP in `infra/vpc/gcp_vpc.py`
- [X] T024 [US3] Implement isolation rules for the database tier (FR-008) across all providers
- [X] T025 [US3] Implement load balancer ingress rules (FR-006) across all providers

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Code Consistency, Policy Linting, and Simulated Dry-Runs (Priority: P4)

**Goal**: Perform automated static checks and configuration simulation plans.

**Independent Test**: Run `pytest tests/vpc/` and `pulumi preview` to ensure zero format anomalies or configuration faults.

### Implementation for User Story 4

- [X] T026 [US4] Create mock-based unit tests for AWS VPC in `tests/vpc/test_aws_vpc.py`
- [X] T027 [US4] Create mock-based unit tests for Azure VPC in `tests/vpc/test_azure_vpc.py`
- [X] T028 [US4] Create mock-based unit tests for GCP VPC in `tests/vpc/test_gcp_vpc.py`
- [X] T029 [US4] Implement static validation check for core layout dependencies in `infra/vpc/base.py` (FR-009)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T030 [P] Implement mandatory Network Flow Logs for all subnets across all providers (FR-011)
- [X] T031 [P] Ensure all technical documentation (docstrings/comments) is bilingual (FR-DOC-001)
- [X] T032 Run final `quickstart.md` validation scenarios
- [X] T033 Code cleanup and compliance check against Pulumi constitution

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 for subnet infrastructure
- **User Story 3 (P3)**: Depends on US1 for subnet infrastructure
- **User Story 4 (P4)**: Can start after US1 is functional for initial testing

### Parallel Opportunities

- Foundation tasks T005, T006, T007, T008 can run in parallel
- Once Foundation is done, US1 (T010, T011, T012) can run in parallel
- US4 tests (T026, T027, T028) can run in parallel
- Final polish tasks T030, T031 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all provider implementations for US1 subnets together:
Task: "Implement AWS Subnet allocation logic in infra/vpc/aws_vpc.py"
Task: "Implement Azure Virtual Network and Subnet allocation logic in infra/vpc/azure_vpc.py"
Task: "Implement GCP Network and Subnetwork allocation logic in infra/vpc/gcp_vpc.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run `pulumi preview` to confirm 6 subnets in 2 zones.

### Incremental Delivery

1. Foundation ready
2. Add US1 (Subnets) → Test
3. Add US2 (Routing/NAT) → Test
4. Add US3 (Firewalls) → Test
5. Add US4 (Tests/Validation) → Finalize

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
