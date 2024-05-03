from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Form
import httpx
import base64
import os
from ..database import get_db
from ..models import Document, User
from typing import List
from sqlalchemy.orm import Session
from .. import oauth2, schemas
router = APIRouter(prefix="/documents",tags=['Documents'])

@router.get("/", response_model= List[schemas.DocumentOut])
def get_all_documents(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    documents = db.query(Document).all()
    return documents

@router.get("/user/{id}", response_model= list[schemas.DocumentOut])
def get_all_user_documents(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    documents = db.query(Document).filter(Document.user_id == id).all()
    return documents

@router.post("/")
async def save_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    if not file.filename.endswith(('.txt', '.docx', '.pdf')):
        raise HTTPException(status_code= 400, detail="Invalid file format. Please upload .txt, .docx or .pdf files")

    # Extract title from filename
    title = os.path.splitext(file.filename)[0]
    
    # Read file content in binary mode
    file_content = await file.read()

    #Encode file content to base 64
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    print(title, encoded_content)
    
    new_document= Document(title = title, content = encoded_content, user_id = current_user.id)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document

@router.patch('/{id}')
def update_document(id: int, updated_document_data: schemas.DocumentOut, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # create document_update query
    update_query = db.query(Document).filter(Document.id == id)
    # use the query to find the particular document
    document = update_query.first()
    # check if the document exist, if it doesn't raise an exception
    if document == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"document with id: {id} does not exist")
    # update the document with new data if it exists
    update_query.update(updated_document_data.model_dump(), synchronize_session= False)
    db.commit()
    return update_query.first()

@router.delete('/{id}')
def delete_document(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # find a document with the given id
    document =db.query(Document).filter(Document.id == id)    
    # check if the document exist, if it doesn't raise an exception
    if document.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"document with id: {id} does not exist")
    # delete the document
    document.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)