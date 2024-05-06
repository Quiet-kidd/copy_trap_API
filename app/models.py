from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)
    
    documents = relationship("Document", back_populates="owner")
    
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key= True, index= True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User", back_populates="documents")
    report = relationship("Report", uselist= False, back_populates="document")
    
class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key= True, index= True)
    # matched_sources = Column(Text, nullable= True)
    payload = Column(JSON)
    status = Column (String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    document = relationship("Document", back_populates="report")