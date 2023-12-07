import network
from time import sleep

class WiFiManager:
    def __init__(self, ssid="rrrr", password="12345678"):
        self.ssid = ssid
        self.password = password
        self.wifi = network.WLAN(network.STA_IF)
        
    def connect_wifi(self):
        """
        Connect to Wi-Fi network.

        Activates the Wi-Fi interface, connects to the specified network,
        and waits until the connection is established.

        :return: None
        """
        
        if not self.wifi.isconnected():
            # Activate the Wi-Fi interface
            self.wifi.active(True)

            # Connect to the specified Wi-Fi network
            self.wifi.connect(self.ssid, self.password)

            # Wait until the connection is established
            print(f"Connecting to {self.ssid}", end="")
            while not self.wifi.isconnected():
                print(".", end="")
                sleep(1)

            print(" Done")
        else:
            print("Already connected")


    def disconnect_wifi(self):
        """
        Disconnect from Wi-Fi network.

        Deactivates the Wi-Fi interface if active and checks if
        the device is not connected to any Wi-Fi network.

        :return: None
        """
        # Check if the Wi-Fi interface is active
        if self.wifi.active():
            # Deactivate the Wi-Fi interface
           self.wifi.active(False)

        # Check if the device is not connected to any Wi-Fi network
        if not self.wifi.isconnected():
            print("Disconnected")

   