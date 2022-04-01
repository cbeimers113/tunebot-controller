import os
import nmap

from device import Device


def get_network_address():
    """Get the network address to scan with nmap."""
    data = os.popen('ifconfig').read()
    wlan_index = data.find('wl')
    ip_a = None

    if wlan_index != -1:
        # Find the wlan info
        ip_a = data[wlan_index:]

        # Find the inet section
        ip_a = ip_a[ip_a.index('inet '):ip_a.index('netmask')]

        # Chop off uneccesary data
        ip_a = ip_a[5:ip_a.rindex('.')] + '.0/24'

    return ip_a


def get_device_addresses():
    """Get a list of connected devices."""
    devices = []
    nm = nmap.PortScanner()
    nm.scan(get_network_address(), arguments='-sP')['scan']

    for ip_address in nm.all_hosts():
        name = nm[ip_address]
        mac_address = "-"
        manufacturer = "-"
        if 'mac' in name['addresses']:
            mac_address = name['addresses']['mac']
            if mac_address in name['vendor']:
                manufacturer = name['vendor'][mac_address]

        devices.append(Device(name['hostnames'][0]['name'], mac_address, ip_address, manufacturer))

    return devices


if __name__ == '__main__':
    devices = get_device_addresses()

    for device in devices:
        print(f'{device}\n===============\n')
