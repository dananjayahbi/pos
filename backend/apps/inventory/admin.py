"""
Django admin configuration for the Inventory application.

Imports admin registrations from submodules so Django's autodiscovery
picks them up.
"""

from apps.inventory.warehouses.admin import BarcodeScanAdmin  # noqa: F401
from apps.inventory.warehouses.admin import DefaultWarehouseConfigAdmin  # noqa: F401
from apps.inventory.warehouses.admin import POSWarehouseMappingAdmin  # noqa: F401
from apps.inventory.warehouses.admin import StorageLocationAdmin  # noqa: F401
from apps.inventory.warehouses.admin import TransferRouteAdmin  # noqa: F401
from apps.inventory.warehouses.admin import WarehouseAdmin  # noqa: F401
from apps.inventory.warehouses.admin import WarehouseCapacityAdmin  # noqa: F401
from apps.inventory.warehouses.admin import WarehouseZoneAdmin  # noqa: F401
