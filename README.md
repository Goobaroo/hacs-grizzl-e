# Grizzl-E EV Charger Integration for Home Assistant

<p align="center">
  <img src="logo.png" alt="Grizzl-E Logo" width="400">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Home Assistant custom integration for Grizzl-E EV chargers with local network connectivity.

## Features

- Real-time monitoring of charging status
- Current, voltage, and power measurements
- Temperature monitoring
- Session and total energy tracking
- Cost tracking
- WiFi signal strength
- Configurable polling interval (10-300 seconds, default 30)
- No cloud dependency

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/goobaroo/hacs-grizzl-e`
6. Select "Integration" as the category
7. Click "Add"
8. Search for "Grizzl-E EV Charger" and install

### Manual Installation

1. Copy the `grizzl_e` folder to your `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

### Initial Setup

1. Go to Settings -> Devices & Services
2. Click "Add Integration"
3. Search for "Grizzl-E EV Charger"
4. Enter the IP address of your charger (e.g., `192.168.0.220`)
5. Optionally configure the scan interval (default: 30 seconds, range: 10-300 seconds)

### Changing Options

To change the scan interval after setup:

1. Go to Settings -> Devices & Services
2. Find the Grizzl-E integration
3. Click "Configure"
4. Adjust the scan interval
5. Click "Submit" (the integration will reload automatically)

## Sensors

The integration provides the following sensors:

| Sensor | Description | Unit |
|--------|-------------|------|
| Charging State | Current charging state | - |
| Pilot Signal | EVSE pilot signal state | - |
| Set Current | Configured charging current | A |
| Measured Current | Actual charging current | A |
| Voltage | Line voltage | V |
| Power | Charging power | W |
| Temperature 1 | Charger temperature (box) | °C |
| Temperature 2 | Charger temperature (socket) | °C |
| Session Energy | Energy delivered in current session | kWh |
| Session Time | Duration of current session | seconds |
| Total Energy | Total energy delivered | kWh |
| Session Cost | Cost of current session | $ |
| WiFi Signal | WiFi signal strength (disabled by default) | dBm |

## Supported Devices

This integration has been tested with:
- Grizzl-E Classic
- Grizzl-E Club

It should work with any Grizzl-E charger that has local network connectivity and exposes the standard web interface.

## Troubleshooting

### Cannot connect to charger

1. Verify the charger is on your network
2. Ping the IP address to ensure connectivity
3. Check that you can access `http://YOUR_IP/` in a browser
4. Ensure your Home Assistant instance can reach the charger's subnet

### Sensors not updating

1. Check the integration logs in Home Assistant
2. Verify the charger is responding: `curl -X POST http://YOUR_IP/main`
3. Check your configured polling interval (default is 30 seconds)
4. Try reducing the scan interval if you need more frequent updates

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/goobaroo/hacs-grizzl-e/issues).

## License

MIT License
