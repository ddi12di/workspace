from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

def validate_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

