from sqlalchemy import Column,String,ForeignKey,Integer,Boolean
from database import Base
import secrets

class topics(Base):
    __tablename__='topics'
    id=Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(12))
    name = Column(String, index=True)  
    file_id = Column(String, ForeignKey("resources.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    is_manual = Column(Boolean, default=False)  # track manual vs auto
