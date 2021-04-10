import os

SOH = b'\x01'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
EOT = b'\x04'

DEFAULT_PORT_PATH = '/dev/pts/'
USER_HOME = os.environ['HOME'] if os.environ["HOME"] is not None else "~"
