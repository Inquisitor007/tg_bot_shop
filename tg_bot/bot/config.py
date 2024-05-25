from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str

@dataclass
class Payment:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    payment: Payment


def get_config():
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        ),
        payment=Payment(
            token=env('PAYMENT_TOKEN')
        )
    )