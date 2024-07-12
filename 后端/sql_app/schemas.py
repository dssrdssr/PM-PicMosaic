from pydantic import BaseModel

class PicBase(BaseModel):
    picname:str
    owner_id:str
    

class PicCreate(PicBase):
    pass

class Pic(PicBase):
    picid:int
    picname:str
    owner_id:str
    class Config:
        orm_mode = True

class WordBase(BaseModel):
    owner_id:str
    name:str
    word:str
    

class WordCreate(WordBase):
    pass

class Word(WordCreate):
    owner_id:str
    name:str
    word:str
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username:str
    password: str
    

class UserCreate(UserBase):
    pass


class User(UserBase):
    username :str
    password:str
    is_active :str
    authority :str
    pics: list[Pic]=[]

    class Config:
        orm_mode = True
