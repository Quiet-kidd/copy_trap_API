from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File, Form
import httpx
import base64
import uuid
import os
from ..database import get_db
from ..models import Document, User, Scan
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
        
    new_document= Document(title = title, content = encoded_content, user_id = current_user.id)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    # create scan id
    scan_id = str(uuid.uuid4())
    # initialise scan to the database
    new_scan = Scan(scan_id = scan_id, document_id = new_document.id, user_id = current_user.id)
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    print(new_scan)
    # prepare copyleaks headers
    # api_key = JDHKSJDDS9DHBSKHEHKEBDKEWHKEWHWEIE933UDHID933DH3I33E3D9HDHID
    # headers = {
    #     'Authorization': f'Bearer {api_key}',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # # prepare copyleaks payload
    # payload = {
    #     "base64": encoded_content,
    #     "filename": file.filename,
    #     "properties":{
    #         "webhooks": {
    #             "status": f"https://copy-trap-api.onrender.com/report/webhook/{{STATUS}}/{new_document.id}",
    #             "statusHeaders":[
    #                 ['Content-Type', 'application/json'],
    #                 ['Accept', 'application/json']
    #             ]
    #         }
    #     }
    # }
    
    # # initialise scan with copyleaks api
    # ENDPOINT = 'https://api.copyleaks.com/v3/scans/submit/file/{scanId}'
    
    # endpoint_url = ENDPOINT.format(scanId= scan_id)
    # async with httpx.AsyncClient() as client:
    #     response = await client.put(endpoint_url, headers=headers, json=payload)
            
    # print(response)       
    # return response```
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