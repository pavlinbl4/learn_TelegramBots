# pip install python-dotenv
import os
from dotenv import load_dotenv, find_dotenv


class Credentials:

    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        self.crazypythonbot = os.getenv('CRAZYPYTHONBOT')
        self.pavlinbl4_bot = os.getenv('PAVLINBL4_BOT')
        self.admin = os.getenv('ADMIN_ID')
        


if __name__ == '__main__':
    assert Credentials().admin == '187597961'