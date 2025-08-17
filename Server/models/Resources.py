from sqlalchemy import Integer,String,Column,ForeignKey,Text
from database import Base
import secrets


class resources(Base):
    __tablename__ = 'resources' 
    id = Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(12))
    resource_url = Column(String, index=True)
    resource_text = Column(Text)
    user_id = Column(String,ForeignKey('users.id'), index=True)