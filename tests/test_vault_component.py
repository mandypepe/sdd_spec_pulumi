import pytest
from infra.vault.aws_vault import AwsVaultComponent

def test_aws_vault_configuration():
    vault = AwsVaultComponent("test-vault")
    
    # Test base class methods implemented in T009/T010/T011/T012
    key_id = vault.configure_master_encryption_key(rotation_days=30)
    assert key_id == "mock-key-id"
    
    firewall = vault.configure_network_firewall(["10.0.0.0/24"])
    assert firewall["firewall"] == ["10.0.0.0/24"]
    
    mapping = vault.map_workload_identity("prod", "sa", "reader")
    assert mapping["namespace"] == "prod"
    
    token = vault.execute_token_exchange("test-token")
    assert token == "mock-ephemeral-token"
