import os

current_dir, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(current_dir, '..', '..', '..')

MESSENGER_SERVER_PORT = 6000

MESSAGE_SENT_TEXT = "{cli} Says: {msg}"
