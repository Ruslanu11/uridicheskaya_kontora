from pydantic import BaseModel
from typing import Optional


class ModifyBaseModel(BaseModel):
    id: Optional[int] = 0


class ChangePassword(ModifyBaseModel):
    password: str


class LoginData(ModifyBaseModel):
    login: str
    password: str


class Post(ModifyBaseModel):
    post: str
    power_level: int

class User(ModifyBaseModel):
    position: int
    login: str
    password: str

class Client(ModifyBaseModel):
    name: str
    address: str
    phone: str

class Case(ModifyBaseModel):
    client_id: int
    description: str
    status: str

class Document(ModifyBaseModel):
    case_id: int
    title: str
    content: str

class Employee(ModifyBaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str

class Appointment(ModifyBaseModel):
    case_id: int
    employee_id: int
    appointment_date: str
    description: str

class Payment(ModifyBaseModel):
    case_id: int
    amount: float
    payment_date: str
    description: str