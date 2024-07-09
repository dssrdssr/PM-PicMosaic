from sqlalchemy import Column, ForeignKey, String 
from sqlalchemy.orm import relationship 
from .database import Base # 假设这里已经定义了Base基类
 
class User(Base): 
    __tablename__ = "usr" 
    uname = Column(String,primary_key=True)
    password = Column(String)  
    # 0被封号  
    is_active = Column(String, default='1') 
    # 0为普通用户，1为DBA，2为程序员用户  
    authority = Column(String, default='0') 
    pics = relationship("Pic", back_populates="owner") 
 
class Pic(Base): 
    __tablename__ = "pic" 
    picname = Column(String,primary_key=True) 
    owner_id = Column(String, ForeignKey("usr.uname")) # 相应地更改ForeignKey的类型  
    owner = relationship("User", back_populates="pics") 