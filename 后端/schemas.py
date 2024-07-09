from pydantic import BaseModel

class PicBase(BaseModel):
    picname:str
    owner_id:str
    

class PicCreate(PicBase):
    pass

class Pic(PicBase):
    picname:str
    owner_id:str
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    uname:str
    password: str
    

class UserCreate(UserBase):
    pass


class User(UserBase):
    uname :str
    password:str
    is_active :str
    authority :str
    pics: list[Pic]=[]

    class Config:
        orm_mode = True