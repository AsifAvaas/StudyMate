from sqlalchemy import Column,Integer,String,Boolean
from database import Base
import secrets


class users(Base):
    __tablename__='users'
    id = Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(12))
    username=Column(String,index=True)
    email=Column(String,index=True)
    password=Column(String,index=True)
    address=Column(String,index=True)
    profile_pic_url=Column(String,index=True,nullable=True)
