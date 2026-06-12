import pytest
from infra.orchestrator.base import OrchestratorProviderFactory
from infra.orchestrator.aws_k8s import AwsK8sComponent

def test_factory_get_component():
    component = OrchestratorProviderFactory.get_component("aws", "test-aws")
    assert isinstance(component, AwsK8sComponent)

def test_factory_invalid_provider():
    with pytest.raises(ValueError):
        OrchestratorProviderFactory.get_component("invalid", "test-invalid")
