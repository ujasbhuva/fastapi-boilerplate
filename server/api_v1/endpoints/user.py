from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server import crud, schemas
from server.utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from server.utils.common import validate_email_send_otp

from ..deps import get_db

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login", response_model=schemas.RespUser)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=500000)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
    )
    db.close()
    return schemas.RespUser(
        id=user.id,
        email=user.email,
        avatar=user.avatar,
        is_verified=user.is_verified,
        providers=user.providers,
        role=user.role,
        created_at=str(user.created_at),
        updated_at=str(user.updated_at),
        token=schemas.Token(access_token=access_token, token_type="bearer"),
    )


@router.get("/profile")
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/sign-up")
async def sign_up(data: schemas.UserCreateInput, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    user = crud.user.get_by_email(db, email=email)

    if user:
        if user.is_verified:
            raise HTTPException(
                400, "You already have an account with us. please continue with login"
            )

    else:
        hashed_password = get_password_hash(data.password)
        user = crud.user.create(
            db,
            obj_in=schemas.UserBase(email=data.email, hashed_password=hashed_password),
        )

    otp_sent = await validate_email_send_otp(db, email, user.id)
    if otp_sent:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "OTP sent to your email, please verify your email to continue",
            },
        )

    db.close()


@router.post("/verify-otp")
async def verify_otp(data: schemas.VerifyOTP, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    otp_sent = data.otp.lower().strip()

    email_otp_obj = crud.email_otp.get_by_email(db, email=email)
    user_obj = crud.user.get_by_email(db, email=email)
    if not email_otp_obj:
        db.close()
        raise HTTPException(400, "First proceed via sending OTP request.")

    otp = email_otp_obj.otp
    time_now = datetime.utcnow()

    if (((time_now - email_otp_obj.updated_at).total_seconds()) / 60) < 10:
        if str(otp_sent) == str(otp):
            user_obj = crud.user.update(
                db, db_obj=user_obj, obj_in=schemas.UserUpdate(is_verified=True)
            )
            crud.email_otp.remove(db, id=email_otp_obj.id)
            db.close()
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "OTP matched, please proceed further.",
                },
            )
        else:
            db.close()
            raise HTTPException(400, "OTP mismatched, Please provide correct OTP.")
    else:
        crud.email_otp.remove(db, id=email_otp_obj.id)
        db.close()
        raise HTTPException(400, "OTP is expired, please proceed new OTP.")
