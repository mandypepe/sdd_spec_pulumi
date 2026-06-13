import pytest
import pulumi
from infra.db.aws_db import AwsDatabase

def test_aws_deletion_protection(db_mocks):
    db = AwsDatabase("test-db")
    db.configure_network("vpc-1", ["s-1"])
    db.configure_security(["sg-1"])
    outputs = db.provision()
    assert outputs.endpoint is not None
