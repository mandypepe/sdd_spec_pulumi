"""
🇪🇸 Programa Pulumi de entrada para desplegar una VPN multi-cloud.
Coordina la creación de recursos usando la configuración tipada y la fábrica de proveedores.

🇺🇸 Pulumi entry point for deploying a multi-cloud VPN.
Coordinates resource creation using typed configuration and the provider factory.
"""

import pulumi
from infra.config import config
from infra.providers import VpnProviderFactory

# Obtener el proveedor desde la configuración centralizada
provider_name = config.provider

# Usar la fábrica para crear el componente VPN específico
vpn_component = VpnProviderFactory.create(
    provider_name=provider_name,
    name=config.vpn_name,
    opts=pulumi.ResourceOptions()
)

# Exportar salidas del stack
pulumi.export("cloud_provider", provider_name)
pulumi.export("vpn_resource_name", vpn_component.resource_name)
pulumi.export("vpn_outputs", vpn_component.get_outputs())
