from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from ..models import Report
from .. import oauth2, schemas
from sqlalchemy.orm import Session


router = APIRouter(prefix="/reports",tags=['Reports'])


@router.get("/", response_model= schemas.ReportOut)
def get_all_reports(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    report = db.query(Report).all()
    return report

@router.post("/webhook/{status}/{document_id}" , response_model= schemas.ReportOut)
def save_report(status: str, document_id: str, payload: dict, db: Session = Depends(get_db)):
    new_report = Report(status = status, document_id = document_id, payload = payload)
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