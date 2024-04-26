from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from .database import engine, get_db
from . import models, schemas
from . import utils
from .routes import documents_routes, reports_routes, auth_route

models.Base.metadata.create_all(bind=engine)

app= FastAPI()


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