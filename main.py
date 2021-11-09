#Python
from typing import Optional
from fastapi.param_functions import Query

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query #clase que permite decir que un parametro de una clase es de tipo Body y Query


app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hai_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    #retornamos un JSON
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    #Body(...) indica que el parametro es obligatorio
    return person

# Validations : Query Parameters

@app.get("/person/detail")
def show_person(
    #parametro name opcional y se valida que minimo tenga un caracter y max 50 y como defailt None
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    #parametro age obligatorio y se valida que minimo tenga un caracter y max 50 y como defailt None
    age: str = Query(...)
):
    return {name: age}