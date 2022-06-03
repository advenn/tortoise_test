TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": "",
                "host": "127.0.0.1",
                "password": "tortoise",
                "port": 5432,
                "user": "tortoise",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models.models"],
            "default_connection": "default",
        }
    },
}
