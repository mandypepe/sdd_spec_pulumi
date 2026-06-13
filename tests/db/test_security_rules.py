import pytest
import pulumi
from infra.db.aws_db import AwsDatabase

def test_aws_security_groups(db_mocks):
    db = AwsDatabase("test-db")
    db.configure_security(["sg-authorized"])
    assert db.security_group is not None
