import random

import psycopg2
from tortoise import Tortoise

from cnf import TORTOISE_ORM

root_user = "postgres://postgres:1@localhost:5432/postgres"
saver = "saver"
conn = psycopg2.connect(root_user)
cur = conn.cursor()
tortoise_cred = "tortoise"
saver_conn = psycopg2.connect(f"postgres://saver:saver@localhost:5432/saver")
saver_cur = saver_conn.cursor()
saver_conn.autocommit = True
conn.autocommit = True
# conn.close()
# saver_conn.close()


def create_random_string():
    letters = "abcdefghijklmnopqrstuvwxyz"
    letters_upper = letters.upper()
    numbers = "0123456789"
    length = 10
    user = ""
    for i in range(length):
        lower_or_upper = random.choice([0, 1])
        if lower_or_upper == 0:
            user += letters[random.randint(0, 25)]
        else:
            user += letters_upper[random.randint(0, 25)]
    password = ""
    for i in range(length):
        lower_or_upper = random.choice([0, 1])
        if lower_or_upper == 0:
            password += letters[random.randint(0, 25)]
        else:
            password += letters_upper[random.randint(0, 25)]
        password += numbers[random.randint(0, 9)]
    db_name = ""
    for i in range(length):
        lower_or_upper = random.choice([0, 1])
        if lower_or_upper == 0:
            db_name += letters[random.randint(0, 25)]
        else:
            db_name += letters_upper[random.randint(0, 25)]
    return user, password, db_name


def create_new_db(db_name, user_name, password):
    cur.execute(f"CREATE USER {tortoise_cred} WITH ENCRYPTED PASSWORD '{tortoise_cred}';")
    cur.execute(f"CREATE DATABASE {db_name} OWNER {tortoise_cred};")
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user_name};")
    print(f"CREATE USER {user_name} WITH ENCRYPTED PASSWORD '{password}';")
    print(f"CREATE DATABASE {db_name};")
    print(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user_name};")

    conn.commit()


saver_cur.execute(f"""CREATE TABLE IF NOT EXISTS saver( 
                   id SERIAL PRIMARY KEY,
                   db_name VARCHAR(255) NOT NULL,
                   db_username VARCHAR(255) NOT NULL,
                   db_pass VARCHAR(255) NOT NULL)"""
                  )


def save_db(db_name, user_name, password):
    saver_cur.execute(
        f"INSERT INTO saver (db_name, db_username, db_pass) VALUES ('{db_name}', '{user_name}', '{password}')")


def delete_credential(db_name):
    saver_cur.execute(f"DELETE FROM saver WHERE db_name = '{db_name}'")


def get_credentials(db_name):
    saver_cur.execute(f"SELECT * FROM saver WHERE db_name = '{db_name}'")
    return cur.fetchone()


def get_all_credentials():
    saver_cur.execute("SELECT * FROM saver;")
    return saver_cur.fetchall()


def delete_db(db_name):
    cur.execute(f"DROP DATABASE {db_name};")
    cur.execute(f"DROP USER {db_name};")
    conn.commit()


def create_databases():
    for i in range(10):
        user, password, db_name = create_random_string()
        print(f"{user} {password} {db_name}")
        create_new_db(db_name=db_name, user_name=tortoise_cred, password=tortoise_cred)
        save_db(db_name=db_name, user_name=user, password=password)


# create_databases()
# print(get_all_credentials())


async def create_tables_with_tortoise():
    for i in get_all_credentials():
        print(i)
        index = i[0]
        db_name = i[1]
        user = i[2]
        password = i[3]
        print(f"{index} {db_name} {user} {password}")
        config = TORTOISE_ORM
        config["connections"]["default"]["credentials"]["database"] = db_name
        config["connections"]["default"]["credentials"]["user"] = user
        config["connections"]["default"]["credentials"]["password"] = password
        print("config: ", config)
        with open(f'{db_name}.py', 'w') as f:
            f.write(f"""import asyncio
from tortoise import Tortoise
TORTOISE_ORM = {config}\n
async def init_and_generate():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("Tortoise initialized {db_name}")
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(init_and_generate())
# except Exception as e:
#     print(11, e)
            """)
        # os.system(f"python {db_name}.py")
        # os.system(f"aerich init -t {db_name}.TORTOISE_ORM -s {db_name}")
        # os.system(f"aerich init-db  {db_name}.pyproject.toml")
        # os.system("aerich migrate")
        # os.system("aerich upgrade")
        try:
            await Tortoise.init(config=config)
            await Tortoise.generate_schemas()
            await Tortoise.close_connections()
        except Exception as e:
            delete_db(db_name)
            delete_credential(db_name)
            print(e)
            continue


# run_async(create_tables_with_tortoise())

