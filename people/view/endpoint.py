import json
from http import HTTPStatus

from sqlalchemy.orm import Session
from view import retfrombd
from models.core import get_db
from .schemas import LoginRequest
from fastapi import APIRouter, Depends, Response, Request
from auth.jwt_auth import validate_user, generate_jwt, decode_jwt

import jwt

view_data = APIRouter(prefix='/view')


@view_data.get('/all')
def ret_all(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authorization = request.headers.get('authorization', None)
    if authorization is None:
        return Response(status_code=HTTPStatus.UNAUTHORIZED)

    token = authorization.split()[1]

    try:
        payload = decode_jwt(token)
    except jwt.InvalidTokenError:
        return Response(status_code=HTTPStatus.UNAUTHORIZED)

    print(payload['username'], 'made request to /all')

    return retfrombd.get_alldb(db, skip=skip, limit=limit)


@view_data.get('/login_kick')
def login(form: LoginRequest):
    if form.username == 'thisiskick' and form.password == '123':
        token = generate_jwt(form.username)

        return Response(
            status_code=HTTPStatus.OK,
            content=json.dumps({'token': token}),
            media_type='application/json'
        )
    else:
        return Response(
            status_code=HTTPStatus.UNAUTHORIZED,
        )
