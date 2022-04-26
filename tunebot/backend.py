import os
import nmap
import threading
from random import shuffle

from kivy.clock import Clock

from tunebot.device import Device
from tunebot.song import Song
from util.log import Log


class BackEnd:
    """The controller backend."""

    # The backend singleton
    BACKEND = None

    def __init__(self, refresh_frontend):
        """Initialize the controller backend."""
        self._playlist = []
        self._now_playing = None
        self._log = Log()
        self._refreshing = False
        self._refresh_interval_sec = 5 * 60  # Refresh every 5 minutes
        self._users = set()  # Keep track of which users are on the network

        # Call this function after backend refreshing to refresh gui
        self._refresh_frontend = refresh_frontend
        self.refresh(None)  # Perform an initial refresh of the playlist

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

    def refresh(self, _):
        """Refresh the playlist in the background."""
        if not self._refreshing:
            threading.Thread(target=self._refresh).start()

    def get_playlist(self):
        """Get the current playlist."""
        return self._playlist

    def get_now_playing(self):
        """Get the currently playing song."""
        return self._now_playing

    def next_song(self):
        """Move to the next song."""
        if not self._playlist:
            return

        try:
            index = self._playlist.index(self._now_playing)
            index = (index + 1) % len(self._playlist)
            self._now_playing = self._playlist[index]
        except ValueError:
            self._now_playing = self._playlist[0]

    def previous_song(self):
        """Move to the previous song."""
        if not self._playlist:
            return

        try:
            index = self._playlist.index(self._now_playing)
            index = (index - 1) % len(self._playlist)
            self._now_playing = self._playlist[index]
        except ValueError:
            self._now_playing = self._playlist[-1]

    def shuffle(self):
        """Shuffle the playlist."""
        if self._now_playing:
            self._playlist.remove(self._now_playing)

        shuffle(self._playlist)

        if self._now_playing:
            self._playlist = [self._now_playing] + self._playlist

    def _refresh(self):
        """Refresh the playlist."""
        self._refreshing = True
        devices = self._load_connected_devices()
        self._playlist = []
        playlist = []  # The playlist before removing blacklisted songs
        blacklist = []
        found_users = set()

        for device in devices:
            username = device.get_username()

            if username:
                playlist += device.get_playlist()
                blacklist += device.get_blacklist()
                found_users.add(username)

        for song in playlist:
            pl_song = Song(song)

            if pl_song not in blacklist and pl_song.resolve():
                self._playlist.append(pl_song)

        # If we aren't currently playing a song, choose the first one
        if self._now_playing is None and self._playlist:
            self._now_playing = self._playlist[0]

        # Check if user list has changed
        users_changed = False

        for user in found_users:
            if user not in self._users:
                users_changed = True
                self._log.info(f'New user on network: {user}')

        for user in self._users:
            if user not in found_users:
                users_changed = True
                self._log.info(f'User left the network: {user}')

        if users_changed:
            self._users = list(found_users)
            self.shuffle()

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

        if nmap_address:
            nm = nmap.PortScanner()
            try:
                nm.scan(nmap_address, arguments='-sP')['scan']

                # Load devices that are on the network
                for ip_address in nm.all_hosts():
                    hosts = nm[ip_address]
                    device_name = hosts['hostnames'][0]['name']
                    mac_address = "-"
                    manufacturer = "-"

                    if 'mac' in hosts['addresses']:
                        mac_address = hosts['addresses']['mac']

                        if mac_address in hosts['vendor']:
                            manufacturer = hosts['vendor'][mac_address]

                    devices.append(
                        Device(device_name, mac_address,
                               ip_address, manufacturer)
                    )

            # Catch any errors with nmap
            except Exception as e:
                self._log.error('An error occured with nmap:')
                self._log.no_prefix(e)

        return devices
