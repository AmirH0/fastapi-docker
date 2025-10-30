from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import SECURITY_KEY, ALGORITHM
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer


def getcurrentuser(request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="token not faound")

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User id not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="User jwt not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
