class Device:
    """Encapsulate device data."""

    def __init__(self, name, mac_address, ip_address, manufacturer):
        """Initialize a device."""
        self._name = name
        self._mac_address = mac_address
        self._ip_address = ip_address
        self._manufacturer = manufacturer

    def get_name(self):
        """Get the device's name."""
        return self._name

    def get_mac_address(self):
        """Get the device's MAC address."""
        return self._mac_address

    def get_ip_address(self):
        """Get the device's IP address."""
        return self._ip_address

    def get_manufacturer(self):
        """Get the device's manufacturer."""
        return self._manufacturer

    def __str__(self):
        return f'Name: {self._name}\nMAC address: {self._mac_address}\nIP address: {self._ip_address}\nManufacturer: {self._manufacturer}'
