"""Constants for the Grizzl-E EV Charger integration."""

DOMAIN = "grizzl_e"
DEFAULT_NAME = "Grizzl-E Charger"
DEFAULT_SCAN_INTERVAL = 30

CONF_HOST = "host"
CONF_SCAN_INTERVAL = "scan_interval"

# Charging states
STATE_MAP = {
    0: "Power Up",
    1: "Self-Test",
    2: "Standby",
    3: "Car Connected",
    4: "Charging",
    5: "Charging Complete",
    6: "Disabled",
    7: "Error",
}

# Pilot states
PILOT_MAP = {
    0: "12V",
    1: "9V",
    2: "6V",
    3: "3V",
    4: "Error",
}
