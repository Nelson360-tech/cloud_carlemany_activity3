import os

from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{os.getenv('POSTGRES_USER', 'carlemany')}:{os.getenv('POSTGRES_PASSWORD', 'carlemany')}@postgres:5432/{os.getenv('POSTGRES_DB', 'carlemany')}"
    },
    "apps": {
        "models": {
            "models": [
                "app.authentication.models",
                "app.files.models",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db():
    await Tortoise.close_connections()