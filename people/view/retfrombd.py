from sqlalchemy.orm import Session
from models.database import Callback
from requestapi import apicallback

def get_alldb(db: Session, skip: int = 0, limit: int = 100):
	return db.query(Callback).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, id: int):
	return db.query(Callback).filter(Callback.id == id).first()


def update_user(db: Session,id:int, title:str, body:str):
	db1 = get_post_by_id(db=db, id=id)
	db1.title = title
	db1.body = body
	db.commit()
	db.refresh(db1)
	return db1