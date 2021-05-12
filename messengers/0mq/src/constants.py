import os
import sys
current_dir, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(1, GITHUB_DIR)

MESSENGER_SERVER_PROTOCOL = 'tcp'
MESSENGER_SERVER_INTERFACE = '127.0.0.1'
MESSENGER_SERVER_PORT = 5000

CONTACTS = {
    'Alexandre': {
        'protocol': 'tcp',
        'interface': '127.0.0.1',
        'port': 6000
    },

    'Gabrielle': {
        'protocol': 'tcp',
        'interface': '127.0.0.1',
        'port': 6001
    },

    'Gabriel': {
        'protocol': 'tcp',
        'interface': '127.0.0.1',
        'port': 6002
    },

    'Lucas': {
        'protocol': 'tcp',
        'interface': '127.0.0.1',
        'port': 6003
    },
}

TRAILING_NEW_LINE = '\n'
TEXT_MESAGE = "{sender}: {msg}"
MESSAGE_SPACE = TRAILING_NEW_LINE + '-'*45 + TRAILING_NEW_LINE
EMPTY_STRING = ''

RECEPTION_CONFIRMATION_MESSAGE = 'received'
BEYE_MESSAGE = 'Bye'
