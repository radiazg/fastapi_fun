from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    #retornamos un JSON
    return {"Hello": "World"}