"""
🇪🇸 Configuración de mocks para pruebas de Base de Datos.
🇺🇸 Mock configuration for Database tests.
"""

import pytest
import pulumi
import sys
import os

# Ensure infra is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.conftest import MyMocks

@pytest.fixture
def db_mocks():
    """
    🇪🇸 Fixture que configura los mocks de Pulumi para las pruebas de DB.
    🇺🇸 Fixture that configures Pulumi mocks for DB tests.
    """
    pulumi.runtime.set_mocks(
        MyMocks(),
        project="db-test-project",
        stack="test",
        preview=False
    )
    yield
