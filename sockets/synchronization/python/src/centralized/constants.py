import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(CURRENT_DIR, '..','..','..','..','..')

DEFAULT_HOST = '127.0.0.1'

FOO_MESAGE = 'foo'.encode()
BAR_MESAGE = 'bar'.encode()

SERVER_PORT = 5002
CONTROLLER_PORT = 5000