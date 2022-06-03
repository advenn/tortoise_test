from tortoise import Tortoise, run_async
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": "tortoise_template",
                "host": "127.0.0.1",
                "password": "tortoise",
                "port": 5432,
                "user": "tortoise",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas(safe=True)
    print("Tortoise initialized")

# run_async(init())