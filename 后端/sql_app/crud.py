from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session,username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(password=user.password,username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_admin_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(password=user.password,username=user.username,authority='1')
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def modify_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    db_user.password = user.password
    db_user.username = user.username
    db_user.is_active = user.is_active
    db_user.authority = user.authority
    db_user.pics = user.pics
    db.commit()
    db.refresh(db_user)
    return db_user

def drop_user(db:Session,username:str):
    db_user=db.query(models.User).filter(models.User.username ==username).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_user_pic(db: Session,username: str,picname:str):
    pic=db.query(models.Pic).filter(models.Pic.owner_id == username).filter(models.Pic.picname == picname ).first()
    return pic
def get_user_last_pic(db: Session,username: str):
    pic=db.query(models.Pic).filter(models.Pic.owner_id == username).order_by(models.Pic.picid.desc()).first()
    return pic

def show_pics(user: schemas.User,db: Session):
    list1=[]
    for onwer_id,picname in db.query(models.Pic.owner_id,models.Pic.picname):
        if onwer_id==user.username and picname!="":
            list1.append(picname)
    if len(list1)==0:
        return 0
    else:
        return list1

def create_user_pic(db: Session, pic: schemas.PicCreate):
    db_pic = models.Pic(owner_id=pic.owner_id,picname=pic.picname)
    db.add(db_pic)
    db.commit()
    db.refresh(db_pic)
    return db_pic

def drop_file(db:Session,pic: schemas.Pic):
    db_file=db.query(models.Pic).filter(models.Pic.owner_id == pic.owner_id).filter(models.Pic.picname == pic.picname ).first()
    db.delete(db_file)
    db.commit()
    return db_file

def get_words(db: Session, name:str,user: schemas.User):
    return db.query(models.Word).filter(models.Word.owner_id == user.username ).filter(models.Word.name == name ).first()


def create_words(db: Session, name:str,user: schemas.User):
    db_words = models.Word(owner_id=user.username,name=name,word="")
    db.add(db_words)
    db.commit()
    db.refresh(db_words)
    return db_words

def get_word(db: Session, name:str,word:str,user: schemas.User):
    return db.query(models.Word).filter(models.Word.owner_id == user.username ).filter(models.Word.name == name ).filter(models.Word.word == word ).first()


def create_word(db: Session, name:str,word:str,user: schemas.User):
    db_word = models.Word(owner_id=user.username,name=name,word=word)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def show_words(name:str,user: schemas.User,db: Session):
    list1=[]
    for onwer_id,name,word in db.query(models.Word.owner_id,models.Word.name,models.Word.word):
        if onwer_id==user.username and name==name:
            if word!="":
                list1.append(word)
    if len(list1)==0:
        return 0
    else:
        return list1


def drop_words(db:Session,name:str,user:schemas.User):
    db_words=db.query(models.Word).filter(models.Word.owner_id == user.username).filter(models.Word.name == name).first()
    while db_words:
        db.delete(db_words)
        db.commit()
        db_words=db.query(models.Word).filter(models.Word.owner_id == user.username).filter(models.Word.name == name).first()
    return 0

def drop_word(db:Session,user: schemas.User,word:str,name:str):
    db_word=db.query(models.Word).filter(models.Word.owner_id == user.username).filter(models.Word.name == name ).filter(models.Word.word == word).first()
    db.delete(db_word)
    db.commit()
    return db_word
