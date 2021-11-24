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
from fastapi import HTTPException
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
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home path"
    )
def home():
    """
    ## Home

    *This path operation its a home path*
    
    **Parameters:**
    - None
    
    Return a json with Hello Word
    """
    #retornamos un JSON
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )
def create_person(
    person: Person = Body(...)
    ):
    #Body(...) indica que el parametro es obligatorio
    """
    ## Create Person

    *This path operation creates a person in the app and save the information in the database*
    
    **Parameters:**
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, email, card number, hair color, marital status and password
    
    Return a person model with first name, last name, age, email, card number, hair color and marital status
    """
    return person

# Validations : Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show a person detail"
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
    """
    ## Show Person Details

    *This path operation show a person detail from database*
    
    **Parameters:**
    - Request Quey parameter:
        - **name: String** -> A person name
        - **age: String** -> A person age
    
    Return a json with the person name and age
    """
    return {name: age}

# Lista de Personas
persons = [1, 2, 3, 4, 5]

# Validations : Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Validate a person exists"
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
    """
    ## Validate a Person

    *This path operation validate if a person exits on database*
    
    **Parameters:**
    - Request Path parameter:
        - **person_id: int** -> A person id
    
    Return a message if the person exists or not.
    """

    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person does not exists!"
        )
    return {person_id: "It exists"}

# Validations: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Update a person"
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
    """
    ## Update a Person

    *This path operation update a person into database*
    
    **Parameters:**
    - Request Path parameter:
        - **person_id: int** -> A person id
    - Request Body parameter:
        - **person: Person** -> A person model with first name, last name, age, email, card number, hair color, marital status and password
        - **location: Location** -> A location model with city, statte and country.
    
    Return a json with the person  and location model
    """
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
    status_code=status.HTTP_200_OK,
    tags=["Login"],
    summary="Loging user"
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    ## Login a User

    *This path operation loging a user in the app*
    
    **Parameters:**
    - Request Form parameter:
        - **username: string** -> A user name
        - **password: string** -> A password for username
    
    Return a LoginOut model with a username and a message
    """

    #instanciamos la calse LoginOut
    return LoginOut(username=username)

#Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"],
    summary="Contact Form"
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
    """
    ## Contact Form

    *This path operation recibe a contact form and save information into database*
    
    **Parameters:**
    - Request Form parameters:
        - **first_name: string** -> A first name of contact
        - **last_name: string** -> A last name of contact
        - **email: EmailStr** -> A email of contact
        - **message: string** -> A message of contact
    - Request Header parameter:
        - **user_agent: string** -> A user agent text
    - Request Cookie parameter:
        - **ads: string** -> A string navegation cookie
    
    Return a user_agent 
    """

    return user_agent

# Files

@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Image"],
    summary="Upload Image"
    )
def post_image(
    image: UploadFile = File(...)
):
    """
    ## Upload Image

    *This path operation upload an image on app and save into database*
    
    **Parameters:**
    - Request File parameters:
        - **image: UploadFile** -> A file to upload
    
    Return a description of image uploaded as file name, format and size(kb)
    """

    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }