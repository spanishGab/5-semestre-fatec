import os
import sys
current_dir, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(1, GITHUB_DIR)

MESSENGER_SERVER_PORT = 5000

CONTACTS_PORTS = {
    'Alexandre': 6000,
    'Gabrielle': 6001,
    'Gabriel': 6002
}

TRAILING_NEW_LINE = '\n'
TEXT_MESAGE = "{cli} Says: {msg}"
MESSAGE_SPACE = '-'*45 + TRAILING_NEW_LINE
EMPTY_STRING = ''

RECEPTION_CONFIRMATION_MESSAGE = b'received'

