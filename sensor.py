"""Sensor platform for Grizzl-E EV Charger."""
from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PILOT_MAP, STATE_MAP
from .coordinator import GrizzlECoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class GrizzlESensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[dict], StateType]


@dataclass
class GrizzlESensorEntityDescription(
    SensorEntityDescription, GrizzlESensorEntityDescriptionMixin
):
    """Describes Grizzl-E sensor entity."""


SENSORS: tuple[GrizzlESensorEntityDescription, ...] = (
    GrizzlESensorEntityDescription(
        key="state",
        name="Charging State",
        icon="mdi:ev-station",
        value_fn=lambda data: STATE_MAP.get(data.get("state"), "Unknown"),
    ),
    GrizzlESensorEntityDescription(
        key="pilot",
        name="Pilot Signal",
        icon="mdi:sine-wave",
        value_fn=lambda data: PILOT_MAP.get(data.get("pilot"), "Unknown"),
    ),
    GrizzlESensorEntityDescription(
        key="currentSet",
        name="Set Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("currentSet"),
    ),
    GrizzlESensorEntityDescription(
        key="curMeas1",
        name="Measured Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("curMeas1"),
    ),
    GrizzlESensorEntityDescription(
        key="voltMeas1",
        name="Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("voltMeas1"),
    ),
    GrizzlESensorEntityDescription(
        key="powerMeas",
        name="Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("powerMeas"),
    ),
    GrizzlESensorEntityDescription(
        key="temperature1",
        name="Temperature 1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("temperature1"),
    ),
    GrizzlESensorEntityDescription(
        key="temperature2",
        name="Temperature 2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("temperature2"),
    ),
    GrizzlESensorEntityDescription(
        key="sessionEnergy",
        name="Session Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda data: data.get("sessionEnergy"),
    ),
    GrizzlESensorEntityDescription(
        key="sessionTime",
        name="Session Time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:timer",
        value_fn=lambda data: data.get("sessionTime"),
    ),
    GrizzlESensorEntityDescription(
        key="totalEnergy",
        name="Total Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda data: data.get("totalEnergy"),
    ),
    GrizzlESensorEntityDescription(
        key="sessionMoney",
        name="Session Cost",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        icon="mdi:currency-usd",
        value_fn=lambda data: data.get("sessionMoney"),
    ),
    GrizzlESensorEntityDescription(
        key="RSSI",
        name="WiFi Signal",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement="dBm",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.get("RSSI"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Grizzl-E sensors."""
    coordinator: GrizzlECoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        GrizzlESensor(coordinator, description) for description in SENSORS
    )


class GrizzlESensor(CoordinatorEntity[GrizzlECoordinator], SensorEntity):
    """Representation of a Grizzl-E sensor."""

    entity_description: GrizzlESensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GrizzlECoordinator,
        description: GrizzlESensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"

        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.entry.entry_id)},
            "name": coordinator.entry.title,
            "manufacturer": "Grizzl-E",
            "model": coordinator.data.get("model", "Unknown"),
            "sw_version": coordinator.data.get("verFWMain", "Unknown"),
        }

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
