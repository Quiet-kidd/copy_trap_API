from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from ..models import Report
from .. import oauth2
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/reports",tags=['Reports'])

class ReportCreate(BaseModel):
    # matched_sources: Optional[str] = None
    similarity_percentage: int
    document_id: int
    
@router.get("/")
def get_all_reports(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    report = db.query(Report).all()
    return report

@router.post("/")
def save_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report_data.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report



@router.delete('/{id}')
def delete_report(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # find a document with the given id
    report =db.query(Report).filter(Report.id == id)    
    # check if the document exist, if it doesn't raise an exception
    if report.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"document with id: {id} does not exist")
    # delete the document
    report.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)