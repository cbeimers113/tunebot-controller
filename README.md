# Tunebot Controller

This is the controller for Tunebot. It uses the [Tunebot API](https://github.com/bronson-g/tunebot-api).

### Requirements
- python 3
- nmap
- vlc
- pulseaudio

To install these packages:
`sudo apt install python3 nmap vlc pulseaudio`

### Python Requirements
These are all listed in requirements.txt
To install these packages:
`pip3 install -r requirements.txt`

### Run the Controller
The controller must be run as root to allow nmap to find devices on the network.
`sudo python3 main.py`

### Issues
The controller does not currently play audio