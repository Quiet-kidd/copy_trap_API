from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from .database import engine
from . import models
from .routes import documents_routes, reports_routes, auth_route

models.Base.metadata.create_all(bind=engine)

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


@app.get("/")
def home_page():
    return  "hello world"   

app.include_router(documents_routes.router)
app.include_router(reports_routes.router)
app.include_router(auth_route.router)