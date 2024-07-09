from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session,uname: str):
    return db.query(models.User).filter(models.User.uname == uname).first()



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(password=user.password,uname=user.uname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def modify_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.uname == user.uname).first()
    db_user.password = user.password
    db_user.uname = user.uname
    db_user.is_active = user.is_active
    db_user.authority = user.authority
    db_user.pics = user.pics
    db.commit()
    db.refresh(db_user)
    return db_user

def drop_user(db:Session,uname:str):
    db_user=db.query(models.User).filter(models.User.uname ==uname).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_user_pic(db: Session,uname: str,picname:str):
    pic=db.query(models.Pic).filter(models.Pic.owner_id == uname).filter(models.Pic.picname == picname ).first()
    return pic

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
