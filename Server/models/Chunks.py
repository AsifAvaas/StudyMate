from sqlalchemy import Integer,String,Column,Text,ForeignKey
from pgvector.sqlalchemy import VECTOR
import secrets
from database import Base

class chunks(Base):
    __tablename__='chunks'
    id = Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(12))
    file_id = Column(String, ForeignKey("resources.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    chunk_text=Column(Text)
    embedding = Column(VECTOR(384)) 
    topic_id = Column(String, ForeignKey("topics.id"), nullable=True) 
