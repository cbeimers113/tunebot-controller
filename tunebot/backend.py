import os
import nmap
import threading

from kivy.clock import Clock

from tunebot.device import Device
from util.log import Log


class BackEnd:
    """The controller backend."""

    # The backend singleton
    BACKEND = None

    def __init__(self, refresh_frontend):
        """Initialize the controller backend."""
        self.playlist = set()
        self._log = Log()
        self._refreshing = False
        self._refresh_interval_sec = 5 * 60  # Refresh every 5 minutes

        # Call this function after backend refreshing to refresh gui
        self._refresh_frontend = refresh_frontend
        self.refresh()  # Perform an initial refresh of the playlist

    def set_refresh_interval_sec(self, refresh_interval_sec):
        """Set the interval in seconds at which the controller scans for users."""
        if refresh_interval_sec < 5:
            self._log.warn(
                f'Refresh interval of {refresh_interval_sec} seconds is too short!')
        else:
            self._refresh_interval_sec = refresh_interval_sec

    def get_refresh_interval_sec(self):
        """Get the refresh interval."""
        return self._refresh_interval_sec

    def refresh(self):
        """Refresh the playlist in the background."""
        if not self._refreshing:
            threading.Thread(target=self._refresh).start()

    def _refresh(self):
        """Refresh the playlist."""
        self._refreshing = True
        devices = self._load_connected_devices()
        self.playlist = set()
        playlist = []  # The playlist before removing blacklisted songs
        blacklist = []

        for device in devices:
            playlist += device.get_playlist()
            blacklist += device.get_blacklist()

        for song in playlist:
            if song not in blacklist:
                self.playlist.add(song)

        self._refreshing = False
        Clock.schedule_once(self._refresh_frontend)

    def _get_nmap_address(self):
        """Get the network address to scan with nmap."""
        data = os.popen('ifconfig').read()
        wlan_index = data.find('wl')
        ip_a = None

        # If we're on a wireless network, extract the network address
        if wlan_index != -1:
            ip_a = data[wlan_index:]
            ip_a = ip_a[ip_a.index('inet '):ip_a.index('netmask')]
            ip_a = ip_a[5:ip_a.rindex('.')] + '.0/24'

        return ip_a

    def _load_connected_devices(self):
        """Get a list of connected devices."""
        nmap_address = self._get_nmap_address()
        devices = [
            Device('test_device', 'AA:BB:CC:DD:EE:FF',
                   '192.168.0.1', 'Ingvonic Studios')
        ]

        # if nmap_address:
        #     nm = nmap.PortScanner()
        #     try:
        #         nm.scan(nmap_address, arguments='-sP')['scan']

        #         # Load devices that are on the network
        #         for ip_address in nm.all_hosts():
        #             hosts = nm[ip_address]
        #             device_name = hosts['hostnames'][0]['name']
        #             mac_address = "-"
        #             manufacturer = "-"

        #             if 'mac' in hosts['addresses']:
        #                 mac_address = hosts['addresses']['mac']

        #                 if mac_address in hosts['vendor']:
        #                     manufacturer = hosts['vendor'][mac_address]

        #             devices.append(
        #                 Device(device_name, mac_address,
        #                        ip_address, manufacturer)
        #             )

        #     # Catch any errors with nmap
        #     except Exception as e:
        #         self._log.error('An error occured with nmap:')
        #         self._log.no_prefix(e)

        return devices
