from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str

@dataclass
class Payment:
    token: str

@dataclass
class RedisConfig:
    host: str
    port: int

@dataclass
class Config:
    tg_bot: TgBot
    payment: Payment
    redis: RedisConfig


def get_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        ),
        payment=Payment(
            token=env('PAYMENT_TOKEN')
        ),
        redis=RedisConfig(
            host=env('REDIS_HOST'),
            port=env.int('REDIS_PORT')
        )
    )