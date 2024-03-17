from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import Callback
from requestapi import apicallback
from models.core import get_db
from view import retfrombd

get_data = APIRouter(prefix='/get')



@get_data.get('/upgrade')
def get_all_posts(db: Session = Depends(get_db)):
	if db.query(Callback).scalar() is not None:
		db.query(Callback).delete()
		db.commit()
	data_list = apicallback.get_all()
	for data_dict in data_list:
		people = Callback(user_id=data_dict['userId'], id=data_dict['id'], title=data_dict['title'],
		                   body=data_dict['body'])
		db.add(people)
	db.commit()


@get_data.get('/delete')
def get_all_posts(db: Session = Depends(get_db)):
	db.query(Callback).delete()
	db.commit()

