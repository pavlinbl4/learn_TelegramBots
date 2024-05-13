from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings():
    load_dotenv()

    return Settings(bots=Bots(
        bot_token=os.getenv('pavlinbl4_bot'),
        admin_id=os.getenv('ADMIN_ID'))
    )


settings = get_settings()
# print(settings)
