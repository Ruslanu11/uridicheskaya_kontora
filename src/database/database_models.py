from peewee import *  
import settings


db = SqliteDatabase(database=f'{settings.DATABASE_PATH}/{settings.DATABASE_NAME}')


class BaseModel(Model):
    class Meta:
        database = db


class Position(BaseModel):
    post = CharField(default='')
    power_level = IntegerField(default=0)
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'post'


class User(BaseModel):
    position_id = ForeignKeyField(Position, backref='users', default=0)
    login = CharField(default='')
    password = CharField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'login'


class Client(BaseModel):
    name = CharField(default='')
    address = CharField(default='')
    phone = CharField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'name'


class Case(BaseModel):
    client_id = ForeignKeyField(Client, backref='cases', default=0)
    description = TextField(default='')
    status = CharField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'status'


class Document(BaseModel):
    case_id = ForeignKeyField(Case, backref='documents', default=0)
    title = CharField(default='')
    content = TextField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'title'


class Employee(BaseModel):
    user_id = ForeignKeyField(User, backref='employees', default='')
    full_name = CharField(default='')
    email = CharField(default='')
    phone = CharField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'full_name'

class Appointment(BaseModel):
    case_id = ForeignKeyField(Case, backref='appointments', default=0)
    employee_id = ForeignKeyField(Employee, backref='appointments', default=0)
    appointment_date = CharField(default='')
    description = TextField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'appointment_date'

class Payment(BaseModel):
    case_id = ForeignKeyField(Case, backref='payments', default=0)
    amount = IntegerField(default=0)
    payment_date = CharField(default='')
    description = TextField(default='')
    class Meta:
        database = db
        power_level = 0
        identifier_field = 'amount'

db_models = [User, Position, Client, Case, Document, Employee, Appointment, Payment]

db.create_tables(db_models)
