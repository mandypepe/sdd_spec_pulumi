import pytest
import pulumi
from infra.vault.factory import VaultProviderFactory
from infra.vault.base import VaultComponentResource

# Mock component
class MockVaultComponent(VaultComponentResource):
    def __init__(self, name, opts=None):
        super().__init__("custom:vault:Mock", name, opts=opts)
    def provision_storage(self, availability_zones, non_destruction=True): pass
    def configure_security(self, allowed_subnets): pass
    def configure_identity_federation(self, trust_provider_url, allowed_namespaces): pass
    def register_secret_blueprint(self, path, target_db_host, ttl_minutes=60): pass

def test_vault_factory_registration():
    VaultProviderFactory.register("mock", MockVaultComponent)
    component = VaultProviderFactory.get_component("mock", "test-vault")
    assert isinstance(component, MockVaultComponent)

def test_vault_factory_unknown_provider():
    with pytest.raises(ValueError):
        VaultProviderFactory.get_component("unknown", "test-vault")
