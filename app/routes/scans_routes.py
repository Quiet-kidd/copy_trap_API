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

router = APIRouter(prefix="/scans",tags=['Scans'])

@router.get("/user/{id}", response_model= List[schemas.ScanOut])
def get_all_scans(id: int, db: Session = Depends(get_db)):
    scans = db.query(Scan).filter(Scan.user_id == id).all()
    return scans