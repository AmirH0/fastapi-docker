from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.redis import check_login_attempts, register_failed_attempt, reset_attempts
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_acces_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Response


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="dosent exist")

    new_user = User(
        username=user.username,
        email=user.email,
        hashpassword=hash_password(user.password),
        display_name=user.display_name,
        is_admin=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(
    data_user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None,
):
    user = db.query(User).filter(User.username == data_user.username).first()

    if not check_login_attempts(data_user.username):
        raise HTTPException(
            status_code=403,
            detail=f"تعداد تلاش‌های مجاز تمام شد، دقیقه بعد دوباره امتحان کنید",
        )

    if not user or not verify_password(data_user.password, user.hashpassword):
        register_failed_attempt(data_user.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    reset_attempts(data_user.username)
    access_token = create_acces_token({"user_id": user.id})

    # response.set_cookie(
    #     key="access_token",
    #     value=f"Bearer {access_token}",
    #     httponly=True,
    #     samesite="lax",

    # )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,
    )

    return {"access_token": access_token, "message": "Logged in"}
