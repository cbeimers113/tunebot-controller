import json
import requests

from util.log import Log


class Device:
    """Encapsulate device data and associate with a playlist/blacklist."""

    def __init__(self, device_name, mac_address, ip_address, manufacturer):
        """ Initialize a device."""
        self._username = None
        self._device_name = device_name
        self._mac_address = mac_address
        self._ip_address = ip_address
        self._manufacturer = manufacturer
        self._playlist = []
        self._blacklist = []
        self._log = Log()
        self._load_user()

    def _load_user(self):
        """Request the account data associated with this MAC address."""
        try:
            # url = 'http://tunebot-api.graansma.dev:8080/device/user/get/'
            # data = requests.post(
                # url, data='{' + f'\n\t"mac": "{self._mac_address}"' + '\n}', timeout=3).json()

            data = None

            with open('test/receive.json', 'r') as f:
                data = json.load(f)

            # If the received object contains an error code, there is no user associated with this device
            if not data or 'error' in list(data.keys()):
                return

            self._username = data['username']
            self._log.info(
                f'Found user {self._username} on {self._device_name}')
            blacklist_enabled = data['blacklist']['enabled']

            # Load the user's blacklist
            if blacklist_enabled:
                self._log.info('Loading blacklist...')

                for song in data['blacklist']['songs']:
                    bl_song = song['url']

                    if bl_song not in self._blacklist:
                        self._blacklist.append(bl_song)
            else:
                self._log.warn(
                    f'{self._username}\'s blacklist was not enabled, not considering')

            # Load the user's playlist
            self._log.info('Loading playlist...')

            for playlist in data['playlists']:
                playlist_enabled = playlist['enabled']
                playlist_name = playlist['name']

                if playlist_enabled:
                    for song in playlist['songs']:
                        url = song['url']

                        if url in self._blacklist and blacklist_enabled:
                            self._log.warn(
                                f'Found "{url}" in both {self._username}\'s playlist "{playlist_name}" and blacklist!')
                            continue

                        pl_song = url

                        if pl_song not in self._playlist:
                            self._playlist.append(pl_song)

                    self._log.info(f'Added "{playlist_name}" to playlist')
                else:
                    self._log.warn(
                        f'Playlist "{playlist_name}" was disabled, not adding')

        # Catch any error if we fail to connect to the API
        except requests.exceptions.RequestException as e:
            self._log.error(
                f'Error retrieving user associated with {self._device_name}, could not reach API:')
            self._log.no_prefix(e)

    def get_username(self):
        """Get the device's user's username."""
        return self._username

    def get_device_name(self):
        """Get the device's name."""
        return self._device_name

    def get_mac_address(self):
        """Get the device's MAC address."""
        return self._mac_address

    def get_ip_address(self):
        """Get the device's IP address."""
        return self._ip_address

    def get_manufacturer(self):
        """Get the device's manufacturer."""
        return self._manufacturer

    def get_playlist(self):
        """Return the playlist of the user associated with this device."""
        return self._playlist

    def get_blacklist(self):
        """Return the blacklist of the user associated with this device."""
        return self._blacklist

    def __str__(self):
        return f'Name: {self._device_name}\nMAC address: {self._mac_address}\nIP address: {self._ip_address}\nManufacturer: {self._manufacturer}'
