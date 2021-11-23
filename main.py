#Python
from typing import Optional
from enum import Enum #Crear enueraciones de strings

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt, PaymentCardNumber, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
#clase que permite decir que un parametro de una clase es de tipo Body, Query y Path para los Parameters
from fastapi import status
#Nos permite acceder a los diferentes codigos de status


app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Medellin"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Antioquia"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="COL"
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    age: PositiveInt = Field(
        ...)
    email: EmailStr = Field(...)
    card_number: Optional[PaymentCardNumber]
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonBase):
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Ricardo",
                "last_name": "Diaz",
                "age": 20,
                "email": "latis@hotmail.com",
                "card_number": "4000000000000002",
                "hair_color": "black",
                "is_married": True,
                "password": "rad123ra"
            }
        }

class PersonOut(PersonBase):
   pass

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="ricky2021"
    )
    message: str = Field(
        default="Login Succesfully"
    )

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    #retornamos un JSON
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    #Body(...) indica que el parametro es obligatorio
    return person

# Validations : Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    #parametro name opcional y se valida que minimo tenga un caracter y max 50 y como defailt None
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is a person name. It's between 1 and 50 characters",
        example="Richard"
        ),
    #parametro age obligatorio y se valida que minimo tenga un caracter y max 50 y como defailt None
    age: str = Query(
        ...,
        title="Person Age",
        description="This is a person age.  It's required",
        example=38
        )
):
    return {name: age}

# Validations : Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is a person ID.  It´s required",
        example=91
        )
):
    return {person_id: "It exists"}

# Validations: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Personal ID",
        description="This is a person ID.  It's required",
        gt=0,
        example=91
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return {
        "person":person,
        "location": location
    }

#Path Operation para enviar datos del formulario
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    #instanciamos la calse LoginOut
    return LoginOut(username=username)

#Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=30,
        min_length=1,
        example='Ricardo'

    ),
    last_name: str = Form(
        ...,
        max_length=30,
        min_length=1,
        example='Diaz'
    ),
    email: EmailStr = Form(..., example='ricardo@diaz.com'),
    message: str = Form(
        ...,
        max_length=50,
        min_length=20,
        example='Hello, your project is very interesting, please call me for an oportunity of venture capital'
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Files

@app.post(
    path="/post-image"
    )
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }