"""
ESP32 Wi-Fi Configuration and Connection

This MicroPython script configures and connects an ESP32 microcontroller
to a Wi-Fi network. It includes functions to connect, disconnect,
and display Wi-Fi configuration details.

Usage:
1. Update the `WIFI_SSID` and `WIFI_PSWD` with your Wi-Fi credentials.
2. Upload and run the script on your ESP32 device.

Authors: Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
         Tomas Fryza
Date: 2023-06-16
"""

import network

# Network settings
WIFI_SSID = "raszvan"
WIFI_PSWD = "12345678"


def connect_wifi(ssid, password):
    """
    Connect to Wi-Fi network.

    Activates the Wi-Fi interface, connects to the specified network,
    and waits until the connection is established.

    :return: None
    """
    from time import sleep_ms

    if not wifi.isconnected():
        # Activate the Wi-Fi interface
        wifi.active(True)

        # Connect to the specified Wi-Fi network
        wifi.connect(ssid, password)

        # Wait until the connection is established
        print(f"Connecting to {ssid}", end="")
        while not wifi.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Done")
    else:
        print("Already connected")


def disconnect_wifi():
    """
    Disconnect from Wi-Fi network.

    Deactivates the Wi-Fi interface if active and checks if
    the device is not connected to any Wi-Fi network.

    :return: None
    """
    # Check if the Wi-Fi interface is active
    if wifi.active():
        # Deactivate the Wi-Fi interface
        wifi.active(False)

    # Check if the device is not connected to any Wi-Fi network
    if not wifi.isconnected():
        print("Disconnected")


# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)

disconnect_wifi()


