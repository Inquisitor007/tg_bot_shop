from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoSettings:
    secret_key: str
    debug: bool


@dataclass
class DataBase:
    name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class RedisDB:
    host: str
    port: int
    db: int


@dataclass
class CeleryData:
    broker_url: str


@dataclass
class Payment:
    token: str


@dataclass
class Config:
    django: DjangoSettings
    db: DataBase
    redis: RedisDB
    celery: CeleryData
    payment: Payment


def get_config(path=None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        django=DjangoSettings(secret_key=env('DJANGO_KEY'),
                              debug=env.bool('DEBUG')),

        db=DataBase(name=env('POSTGRES_DB'),
                    user=env('POSTGRES_USER'),
                    password=env('POSTGRES_PASSWORD'),
                    host=env('POSTGRES_HOST'),
                    port=env.int('POSTGRES_PORT')),

        redis=RedisDB(host=env('REDIS_HOST'),
                      port=env.int('REDIS_PORT'),
                      db=env.int('REDIS_DB')),

        celery=CeleryData(
            broker_url=f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/{env('REDIS_DB')}"
        ),

        payment=Payment(
            token=env('PAYMENT_TOKEN')
        )

    )
