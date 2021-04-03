import os
CURRENT_DIR, _ = os.path.split(os.path.abspath(__file__))
GITHUB_DIR = os.path.join(CURRENT_DIR, '..','..','..','..','..')

DEFAULT_HOST = '127.0.0.1'

FOO_MESAGE = 'foo'.encode()
BAR_MESAGE = 'bar'.encode()