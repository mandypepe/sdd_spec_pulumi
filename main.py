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
# pulumi.export must be called when the program is run by the Pulumi engine
# (e.g. `pulumi up`). Running this file directly with plain `python` will
# raise "Root resource is not an instance of 'Stack'". To make the module
# friendly for both running under Pulumi and executing directly (for quick
# debugging or IDE runs), attempt to export and fall back to printing when
# not executed as a Pulumi program.
try:
    pulumi.export("cloud_provider", provider_name)
    pulumi.export("vpn_resource_name", vpn_component.resource_name)
    pulumi.export("vpn_outputs", vpn_component.get_outputs())
except Exception as e:
    # Likely not running under the Pulumi engine (e.g. `python main.py`).
    # Print a helpful message and the values so an IDE run isn't fatal.
    print("[pulumi export skipped] Not running under Pulumi engine:", str(e))
    print("cloud_provider:", provider_name)
    # vpn_component may be a Pulumi ComponentResource; access attributes carefully
    try:
        print("vpn_resource_name:", getattr(vpn_component, 'resource_name', None))
    except Exception:
        print("vpn_resource_name: <unavailable>")
    try:
        print("vpn_outputs:", vpn_component.get_outputs())
    except Exception:
        print("vpn_outputs: <unavailable>")
