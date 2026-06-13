"""
🇪🇸 Configuración de mocks de Pulumi para pruebas unitarias.
Permite probar lógica de creación de recursos sin conectarse a la nube.

🇺🇸 Pulumi mock configuration for unit testing.
Enables testing resource creation logic without cloud connectivity.
"""

import pytest
import pulumi
import sys
import os
import asyncio

# Asegurar que el directorio raíz está en el path para importar 'infra'
# Ensure root directory is in path to import 'infra'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MyMocks(pulumi.runtime.Mocks):
    """
    🇪🇸 Implementación de mocks de Pulumi para pruebas (Mock Pattern).
    Simula recursos sin efectos colaterales en la nube.
    
    🇺🇸 Pulumi mocks implementation for testing (Mock Pattern).
    Simulates resources without side effects on cloud.
    """

    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        """
        🇪🇸 Simula la creación de un nuevo recurso.
        Retorna un ID simulado basado en el nombre del recurso.
        
        🇺🇸 Simulates creation of a new resource.
        Returns simulated ID based on resource name.
        """
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        """
        🇪🇸 Simula llamadas a funciones de Pulumi (como data sources).
        
        🇺🇸 Simulates calls to Pulumi functions (such as data sources).
        """
        return {}


@pytest.fixture
def pulumi_mocks():
    """
    🇪🇸 Fixture de pytest que configura los mocks de Pulumi antes de cada prueba.
    Establece el contexto de ejecución de prueba (project, stack, preview).
    
    🇺🇸 Pytest fixture that configures Pulumi mocks before each test.
    Sets test execution context (project, stack, preview).
    """
    # Usar el event loop actual si existe, de lo contrario crear uno
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    pulumi.runtime.set_mocks(
        MyMocks(),
        project="test-project",
        stack="test-stack",
        preview=False
    )
    yield
