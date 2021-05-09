import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(CURRENT_DIR, '..','..')

NETWORK_INTERFACE = 'lxdbr0'
INTERFACE_MAC_ADDRESS = b'\xe0\xd5\x5e\xa6\x03\xf1'
ETHERNET_FRAME_TYPE = b'\x88\xb5'
