"""Configuración de mocks para pruebas unitarias de Pulumi.

Permite probar la lógica de creación de recursos sin conectarse a la nube.
"""

import pytest
import pulumi
import sys
import os

# Asegurar que el directorio raíz está en el path para importar 'infra'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MyMocks(pulumi.runtime.Mocks):
    """Implementación de mocks de Pulumi para pruebas."""

    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        # Retorna el nombre del recurso y un ID simulado
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        # Simula llamadas a funciones de Pulumi
        return {}


@pytest.fixture
def pulumi_mocks():
    """Configura los mocks de Pulumi antes de cada prueba."""
    pulumi.runtime.set_mocks(
        MyMocks(),
        project="test-project",
        stack="test-stack",
        preview=False
    )
    yield
