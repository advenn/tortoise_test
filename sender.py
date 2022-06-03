import requests
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette_wtf import StarletteForm
from wtforms import StringField
from wtforms.validators import DataRequired

from cnf import TORTOISE_ORM
from models import models

temp = Jinja2Templates(directory="templates")


class UserForm(StarletteForm):
    name = StringField('name', validators=[DataRequired()])


class AddUserForm(StarletteForm):
    db_name = StringField('db', validators=[DataRequired()])
    id = StringField('id', validators=[DataRequired()])
    user = StringField('user', validators=[DataRequired()])


class AddProductForm(StarletteForm):
    db_name = StringField('db', validators=[DataRequired()])
    id = StringField('id', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    code = StringField('code', validators=[DataRequired()])


app = FastAPI()


@app.get('/')
@app.post('/')
async def get_username(request: Request):
    form = await UserForm.from_formdata(request)
    if request.method == 'POST':
        name = form.name.data
        requests.post(f'http://localhost:5000/create/{name}')
    return temp.TemplateResponse('index.html', {"request": request, 'form': form})


@app.get("/add/")
@app.post("/add/")
async def add_user(request: Request):
    form = await AddUserForm.from_formdata(request)
    if request.method == 'POST':
        requests.post('http://localhost:5000/add/', data=form.db_name.data)





if __name__ == '__main__':
    uvicorn.run("sender:app", debug=True, port=5001, reload=True)
