import pytest
import pulumi
from infra.providers import DatabaseProviderFactory

def test_database_factory_aws(db_mocks):
    db = DatabaseProviderFactory.create("aws", "my-db")
    assert db._name == "my-db"
    assert "AwsDatabase" in str(type(db))

def test_database_factory_azure(db_mocks):
    db = DatabaseProviderFactory.create("azure", "my-db")
    assert db._name == "my-db"
    assert "AzureDatabase" in str(type(db))

def test_database_factory_gcp(db_mocks):
    db = DatabaseProviderFactory.create("gcp", "my-db")
    assert db._name == "my-db"
    assert "GcpDatabase" in str(type(db))
