from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from view import retfrombd
from models.core import get_db
from auth.jwt_auth import validate_user

view_data = APIRouter(prefix='/view')


@view_data.get('/all')
def ret_all(skip: int=0,limit:int=100, db: Session = Depends(get_db), token: str = Depends(validate_user)):
	return retfrombd.get_alldb(db, skip=skip, limit=limit)

@view_data.get('/get/{id}')
def ret_all(id:int ,db: Session = Depends(get_db), token: str = Depends(validate_user)):
	return retfrombd.get_post_by_id(db,id)