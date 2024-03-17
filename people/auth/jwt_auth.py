import time

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

import jwt


def validate_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def generate_jwt(username: str) -> str:
    token = jwt.encode(
        payload={
            'username': username,
            'exp': time.time() + 60 * 10
        },
        key='secret'

    )

    return token.decode(encoding='utf8')


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, key='secret', algorithms=['HS256'])

