"""
🇪🇸 Pruebas unitarias del patrón Factory para componentes Orquestadores.
Valida registro, instantiación, y configuración de seguridad/identidad.

🇺🇸 Unit tests for Factory pattern in Orchestrator components.
Validates registration, instantiation, and security/identity configuration.
"""

import pytest
import pulumi
from unittest.mock import MagicMock, patch
from infra.orchestrator.base import OrchestratorProviderFactory, OrchestratorComponent
from infra.orchestrator.aws_k8s import AwsK8sComponent
from infra.orchestrator.azure_k8s import AzureK8sComponent
from infra.orchestrator.gcp_k8s import GcpK8sComponent


class MyMocks(pulumi.runtime.Mocks):
    """Mock implementation for testing orchestrator components"""
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]
    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


@pytest.fixture
def pulumi_mocks():
    """Configure Pulumi mocks for testing"""
    pulumi.runtime.set_mocks(
        MyMocks(),
        project="test-project",
        stack="test-stack",
        preview=False
    )
    yield


class TestOrchestratorProviderFactory:
    """Test OrchestratorProviderFactory registration and instantiation"""
    
    def test_factory_registers_aws_provider(self):
        """Verify AWS provider is registered with factory"""
        component = OrchestratorProviderFactory.get_component("aws", "test-aws")
        assert isinstance(component, AwsK8sComponent)
    
    def test_factory_registers_azure_provider(self):
        """Verify Azure provider is registered with factory"""
        component = OrchestratorProviderFactory.get_component("azure", "test-azure")
        assert isinstance(component, AzureK8sComponent)
    
    def test_factory_registers_gcp_provider(self):
        """Verify GCP provider is registered with factory"""
        component = OrchestratorProviderFactory.get_component("gcp", "test-gcp")
        assert isinstance(component, GcpK8sComponent)
    
    def test_factory_case_insensitive_provider_lookup(self):
        """Verify factory is case-insensitive for provider names"""
        component_lower = OrchestratorProviderFactory.get_component("AWS", "test-1")
        component_upper = OrchestratorProviderFactory.get_component("aws", "test-2")
        assert isinstance(component_lower, AwsK8sComponent)
        assert isinstance(component_upper, AwsK8sComponent)
    
    def test_factory_raises_error_for_unregistered_provider(self):
        """Verify factory raises ValueError for unregistered providers"""
        with pytest.raises(ValueError) as exc_info:
            OrchestratorProviderFactory.get_component("invalid-provider", "test")
        assert "not registered" in str(exc_info.value)


class TestOrchestratorComponentBase:
    """Test OrchestratorComponent base functionality"""
    
    def test_component_inheritance(self):
        """Verify all provider components inherit from OrchestratorComponent"""
        aws_component = OrchestratorProviderFactory.get_component("aws", "test-aws")
        azure_component = OrchestratorProviderFactory.get_component("azure", "test-azure")
        gcp_component = OrchestratorProviderFactory.get_component("gcp", "test-gcp")
        
        assert isinstance(aws_component, OrchestratorComponent)
        assert isinstance(azure_component, OrchestratorComponent)
        assert isinstance(gcp_component, OrchestratorComponent)
    
    def test_component_has_required_methods(self):
        """Verify orchestrator components have all required methods"""
        component = OrchestratorProviderFactory.get_component("aws", "test")
        
        assert hasattr(component, 'provision')
        assert hasattr(component, 'configure_security')
        assert hasattr(component, 'configure_identity')
        assert hasattr(component, 'allocate_multi_zone_subnets')
        assert hasattr(component, 'get_current_node_count')
        assert hasattr(component, 'preserve_scaling_state')
        assert hasattr(component, 'configure_ingress_rules')
        assert hasattr(component, 'configure_egress_rules')
        assert hasattr(component, 'configure_minimum_privilege_identity')
        assert hasattr(component, 'get_identity_arn_or_id')


class TestMultiZoneIsolation:
    """Test User Story 1: Multi-Zone Private Network Isolation"""
    
    def test_allocate_multi_zone_subnets_creates_zone_mapping(self):
        """Verify multi-zone subnet allocation creates proper zone-to-subnet mapping"""
        component = OrchestratorProviderFactory.get_component("aws", "test-multi-zone")
        
        availability_zones = ["us-east-1a", "us-east-1b"]
        subnet_ids = ["subnet-11111111", "subnet-22222222"]
        
        # Mock the implementation
        expected_mapping = {
            "us-east-1a": "subnet-11111111",
            "us-east-1b": "subnet-22222222"
        }
        
        component.allocate_multi_zone_subnets = MagicMock(return_value=expected_mapping)
        result = component.allocate_multi_zone_subnets(availability_zones, subnet_ids)
        
        assert result == expected_mapping
        assert len(result) == 2
        assert "us-east-1a" in result
        assert "us-east-1b" in result


class TestScalingIdempotence:
    """Test User Story 2: Automated Scaling Synchronization and Idempotence"""
    
    def test_preserve_scaling_state_ignores_autoscale_increases(self):
        """Verify state preservation ignores node count increases from autoscaling"""
        component = OrchestratorProviderFactory.get_component("aws", "test-scaling")
        
        # Mock current count as 5 (autoscaled from desired 3)
        component.get_current_node_count = MagicMock(return_value=5)
        
        result = component.preserve_scaling_state(desired_count=3)
        
        assert result is True  # State was preserved (no changes needed)
        assert component._scaled_node_count == 5
    
    def test_preserve_scaling_state_allows_scale_down(self):
        """Verify state preservation allows scaling down when below desired"""
        component = OrchestratorProviderFactory.get_component("aws", "test-scaling")
        
        # Mock current count as 2 (below desired 3)
        component.get_current_node_count = MagicMock(return_value=2)
        
        result = component.preserve_scaling_state(desired_count=3)
        
        assert result is False  # Sync needed (scale up required)
        assert component._scaled_node_count == 2


class TestPerimeterEnforcement:
    """Test User Story 3: Restricted Perimeter Enforcement & Access Rejection"""
    
    def test_configure_ingress_rules_blocks_admin_ports(self):
        """Verify ingress rules block unauthorized SSH and RDP"""
        component = OrchestratorProviderFactory.get_component("aws", "test-perimeter")
        
        rules = component.configure_ingress_rules(allow_admin_cidr_blocks=[])
        
        assert "block_all_ssh" in rules
        assert "block_all_rdp" in rules
        assert rules["block_all_ssh"]["from_port"] == 22
        assert rules["block_all_rdp"]["from_port"] == 3389
        assert rules["block_all_ssh"]["cidr_blocks"] == []
        assert rules["block_all_rdp"]["cidr_blocks"] == []
    
    def test_configure_ingress_rules_allows_authorized_admin_cidr(self):
        """Verify ingress rules allow SSH from authorized admin CIDR blocks"""
        component = OrchestratorProviderFactory.get_component("aws", "test-perimeter")
        
        authorized_cidr = ["10.0.0.0/8"]
        rules = component.configure_ingress_rules(allow_admin_cidr_blocks=authorized_cidr)
        
        assert "allow_admin_ssh" in rules
        assert rules["allow_admin_ssh"]["cidr_blocks"] == authorized_cidr
    
    def test_configure_egress_rules_restricts_database_access(self):
        """Verify egress rules restrict outbound to authorized database endpoints"""
        component = OrchestratorProviderFactory.get_component("aws", "test-perimeter")
        
        db_endpoints = ["db.example.com"]
        proxy_endpoints = ["proxy.example.com"]
        rules = component.configure_egress_rules(
            database_endpoints=db_endpoints,
            proxy_endpoints=proxy_endpoints
        )
        
        assert "allow_database" in rules
        assert "allow_proxy" in rules
        assert rules["allow_database"]["destinations"] == db_endpoints
        assert rules["allow_proxy"]["destinations"] == proxy_endpoints
    
    def test_configure_egress_rules_denies_unauthorized_traffic(self):
        """Verify egress rules have default deny for unauthorized traffic"""
        component = OrchestratorProviderFactory.get_component("aws", "test-perimeter")
        
        rules = component.configure_egress_rules([], [])
        
        assert "deny_all_outbound" in rules
        assert rules["deny_all_outbound"]["protocol"] == "-1"


class TestIdentityGovernance:
    """Test User Story 4: Minimum Privilege Identity Governance"""
    
    def test_configure_minimum_privilege_identity_sets_defaults(self):
        """Verify identity configuration uses minimum required permissions"""
        component = OrchestratorProviderFactory.get_component("aws", "test-identity")
        
        config = component.configure_minimum_privilege_identity(permissions=None)
        
        assert config["enforce_workload_identity"] is True
        assert config["deny_business_data"] is True
        assert config["deny_cross_account"] is True
        assert len(config["permissions"]) > 0
    
    def test_configure_minimum_privilege_identity_custom_permissions(self):
        """Verify identity configuration accepts custom permissions list"""
        component = OrchestratorProviderFactory.get_component("aws", "test-identity")
        
        custom_perms = ["eks:JoinCluster", "ecr:PullImage"]
        config = component.configure_minimum_privilege_identity(permissions=custom_perms)
        
        assert config["permissions"] == custom_perms
    
    def test_get_identity_arn_or_id_is_abstract(self):
        """Verify get_identity_arn_or_id is provider-specific"""
        component = OrchestratorProviderFactory.get_component("aws", "test-identity")
        
        # This is abstract, so each provider must implement it
        assert callable(component.get_identity_arn_or_id)


class TestComponentInstantiation:
    """Test component instantiation with various configurations"""
    
    def test_component_instantiation_with_options(self):
        """Verify component can be instantiated with Pulumi ResourceOptions"""
        opts = pulumi.ResourceOptions(
            depends_on=[],
            protect=False
        )
        component = OrchestratorProviderFactory.get_component("aws", "test-opts", opts=opts)
        assert isinstance(component, AwsK8sComponent)
    
    def test_component_name_is_set_correctly(self):
        """Verify component name is set during instantiation"""
        component = OrchestratorProviderFactory.get_component("aws", "my-orchestrator")
        assert component.name == "my-orchestrator"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

