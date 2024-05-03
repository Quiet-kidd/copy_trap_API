from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import engine, get_db
from .. import models, schemas
from .. import utils
from ..routes import documents_routes, reports_routes
from .. import oauth2 
models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/auth",tags=['Auth'])

@router.post("/login", response_model=schemas.LoginOut)
def login(loginCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(loginCredentials)
    # use the submitted email to find the user from database
    user = db.query(models.User).filter(models.User.email == loginCredentials.username).first()
    
    # compare the found user's password with the submitted password 
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Invalid email')
    
    if not utils.verify(loginCredentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Invalid credentials')
    # return user only if the password matches,  return an error if the password doesn't match
    
    # create an access token for the user and add it to the response
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return{"access_token": access_token, "token_type": "bearer","user":user}


    # print(loginCredentials)
    # return {f"user with: {loginCredentials.email} and password:{loginCredentials.password} has logged in"}
@router.get("/users", response_model= list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/register", response_model= schemas.UserOut)
def register(registerCredentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # check for an existing user with the submitted email
    existing_user = db.query(models.User).filter(models.User.email == registerCredentials.email).first()
    
    if existing_user:
        raise HTTPException(status_code= status.HTTP_201_CREATED, detail= f'user exists')
    
    # return an error if a user actual exist with that email
    
    # hash the password
    hashed_password = utils.hash(registerCredentials.password)
    # set the value of password to the hashed password
    registerCredentials.password = hashed_password
    # save user with the hashed password 
    new_user = models.User(**registerCredentials.model_dump())
    db.add(new_user)    
    db.commit()
    db.refresh(new_user)
    
    return new_user


    # print(registerCredentials)
    # return {f"name:{registerCredentials.name} user: {registerCredentials.email} phone number:{registerCredentials.phone_number} and password: {registerCredentials.password} has registered"}
    