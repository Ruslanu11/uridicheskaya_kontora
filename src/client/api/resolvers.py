import requests
import settings
from src.database import database_models, pydantic_models
from src.database.database_models import *
import peewee


def login(password: str, login: str) -> dict:
    user = database_models.User.get_or_none((database_models.User.password == password) & (database_models.User.login == login))
    if user:
        return {'code': 200, 'msg': 'Succesfully', 'result': user}

    return {'code': 400, 'msg': 'Not found', 'result': None}

def register(data: pydantic_models.User) -> dict:
    user = database_models.User.create(
        login=data.login,
        password=data.password,
        position_id=data.position
        )
    
    return {'code': 200, 'msg': 'Succesfully', 'result': user}

def update_password(id: int, password: str) -> dict:
    user = database_models.User.get(database_models.User.id == id)

    user.password = password

    user.save()

    return {'code': 200, 'msg': 'Succesfully', 'result': user}

def delete_account(id: int) -> dict:
    user = database_models.User.get(database_models.User.id == id)
    user.delete_instance()

    return {'code': 200, 'msg': 'Succesfully', 'result': None}

def add_action(database_model: peewee.Model, data: dict):
    new_database_model = database_model.create()

    for attr, value in data.items():
        if attr == 'id':
            continue

        if '_id' in attr:
            table = attr.split('_')[0].capitalize()
            query = eval(f"{table}.select({table}.id).dicts()")
            if int(value) not in map(lambda item: item['id'], query):
                new_database_model.delete_instance()
                return False
                        
        setattr(new_database_model, attr, value)
    
    new_database_model.save()
    return True

def upd_action(id: int, database_model: peewee.Model, data: dict):
    model = database_model.get(database_model.id == id)

    for attr, value in data.items():
        if attr == 'id':
            continue

        if '_id' in attr:
            table = attr.split('_')[0].capitalize()
            query = eval(f"{table}.select({table}.id).dicts()")
            if int(value) not in map(lambda item: item['id'], query):
                return False

        setattr(model, attr, value)

    model.save()

    return True


def del_action(id: int, database_model: peewee.Model):
    res = database_model.get_or_none(database_model.id == id)

    if res:
        res.delete_instance()