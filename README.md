# Tunebot Controller

This was the controller for Tunebot. It uses the [Tunebot API](https://github.com/bronson-g/tunebot-api).

### Requirements
- Python 3
- pip for Python 3
- nmap
- vlc
- pulseaudio

By default, nmap and pulseaudio should be installed. \
To install these packages on a Debian distro, execute the following command: \
`sudo apt install python3 python3-pip nmap vlc pulseaudio`

### Python Requirements
These are all listed in requirements.txt \
To install these packages: \
`sudo pip3 install -r requirements.txt`

### Run the Controller
The controller must be run as root to allow nmap to find devices on the network. \
`sudo python3 main.py`
