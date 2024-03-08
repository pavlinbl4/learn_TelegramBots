# pip install python-dotenv
import os
from dotenv import load_dotenv


class Credentials:

    def __init__(self):
        load_dotenv()
        self.api_id = os.environ.get('api_id')
        self.api_hash = os.environ.get('api_hash')
        self.crazypythonbot = os.environ.get('crazypythonbot')
        self.pavlinbl4_bot = os.environ.get('pavlinbl4_bot')