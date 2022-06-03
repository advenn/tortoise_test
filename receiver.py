import os

import psycopg2
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from flask_wtf import FlaskForm
from tortoise import Tortoise
from wtforms import StringField
from wtforms.validators import DataRequired
import uuid
from cnf import TORTOISE_ORM
from models import models
from sender import AddUserForm

"""
1. Create database with specified name
2. user = password = "tortoise"
3. 
"""
temp = Jinja2Templates(directory="templates")


class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


app = FastAPI()


@app.get('/create2/{dbname2}')
@app.post('/create2/{dbname2}')
async def create_db(dbname2: str):
    print(f"dbname2: {dbname2}")


@app.get('/create/{dbname}')
@app.post('/create/{dbname}')
async def create_db(dbname: str):
    print(f"dbname: {dbname}")
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='1',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute(f"CREATE DATABASE {dbname} OWNER tortoise;")
    print(f"Database {dbname} created")
    conf = TORTOISE_ORM
    conf['connections']['default']['credentials']['database'] = dbname
    f = open(f"{dbname}.py", 'w')
    f.write(f"""
from tortoise import Tortoise, run_async
TORTOISE_ORM = {conf}\n
async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas(safe=True)
    print("Tortoise initialized")

run_async(init())""")
    f.close()
    try:
        os.system(f"""
python {dbname}.py""")
        f = open(f"{dbname}.py", 'w')
        conf['apps']['models']['models'].append("aerich.models")
        f.write(f"""
from tortoise import Tortoise, run_async
TORTOISE_ORM = {conf}\n
async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    # await Tortoise.generate_schemas(safe=True)
    print("Tortoise initialized")

# run_async(init())""")
        f.close()
        os.system(f"""
aerich init -t {dbname}.TORTOISE_ORM
aerich upgrade""")

    except Exception as e:
        print(e)


@app.get("/add/")
@app.post("/add/")
async def add_user(request: Request):
    form = await AddUserForm.from_formdata(request)
    if request.method == "POST":
        db_name = form.db_name.data
        id = form.id.data
        user = form.user.data
        print(f"db_name: {db_name}\nid: {id}\nuser: {user}")
        conf = TORTOISE_ORM
        conf['connections']['default']['credentials']['database'] = db_name
        try:
            await Tortoise.init(config=conf)
            await models.User.create(id=uuid.uuid4(), user=user)
            await Tortoise.close_connections()
            print(f"User {user} added to {db_name}")
        except Exception as e:
            print(e)
    return temp.TemplateResponse("add.html", {"form": form, "request": request})


@app.get("/get")
async def get_all():
    dbs = ["asadbek2", "asadbe", 'tortoise_template']
    data = []
    for i in dbs:
        conf = TORTOISE_ORM
        conf['connections']['default']['credentials']['database'] = i
        try:
            await Tortoise.init(config=conf)
            user = await models.User.all()
            data.append(user)
            await Tortoise.close_connections()
        except Exception as e:
            print(e)
    print(data, dbs)



if __name__ == '__main__':
    uvicorn.run("receiver:app", debug=True, port=5000, reload=True)

