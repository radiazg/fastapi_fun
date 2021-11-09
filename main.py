#Python
from typing import Optional
from fastapi.param_functions import Path, Query
from enum import Enum #Crear enueraciones de strings

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path 
#clase que permite decir que un parametro de una clase es de tipo Body, Query y Path para los Parameters


app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    age: int = Field(
        ...,
        gt=0,
        le=115)
    hai_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

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
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is a person name. It's between 1 and 50 characters"
        ),
    #parametro age obligatorio y se valida que minimo tenga un caracter y max 50 y como defailt None
    age: str = Query(
        ...,
        title="Person Age",
        description="This is a person age.  It's required"
        )
):
    return {name: age}

# Validations : Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is a person ID.  It´s required"
        )
):
    return {person_id: "It exists"}

# Validations: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Personal ID",
        description="This is a person ID.  It's required",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results