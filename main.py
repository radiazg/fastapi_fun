#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body #clase que permite decir que un parametro de una clase es de tipo Body


app = FastAPI()

#models

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