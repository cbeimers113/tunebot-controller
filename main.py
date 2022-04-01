from backend.network import load_connected_devices


RUNNING = False

if __name__ == '__main__' and not RUNNING:
    RUNNING = True
    devices = load_connected_devices(debug=True)
