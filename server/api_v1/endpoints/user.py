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
    verify_password,
)
from server.utils.common import validate_email_send_otp

from ..deps import get_db

TOKEN_EXPIRE_DELTA = 20160

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/login", response_model=schemas.RespUser)
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
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_DELTA)
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


@user_router.post("/profile", response_model=schemas.UserProfile)
async def get_profile(current_user=Depends(get_current_user)):
    return schemas.UserProfile(
        id=current_user.id,
        email=current_user.email,
        avatar=current_user.avatar,
        role=current_user.role,
    )


@user_router.post("/sign-up")
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


@user_router.post("/verify-otp")
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
            access_token_expires = timedelta(minutes=TOKEN_EXPIRE_DELTA)
            access_token = create_access_token(
                data={"sub": user_obj.email, "id": user_obj.id},
                expires_delta=access_token_expires,
            )
            db.close()
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Password updated.",
                    "data": {
                        "token": access_token,
                        "token_type": "bearer",
                    },
                },
            )
        else:
            db.close()
            raise HTTPException(400, "OTP mismatched, Please provide correct OTP.")
    else:
        crud.email_otp.remove(db, id=email_otp_obj.id)
        db.close()
        raise HTTPException(400, "OTP is expired, please proceed new OTP.")


@user_router.post("/resend-otp")
async def resend_otp(data: schemas.EmailSchema, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    user_obj = crud.user.get_by_email(db, email=email)
    if not user_obj:
        db.close()
        raise HTTPException(400, "First proceed via sending OTP request.")

    otp_sent = await validate_email_send_otp(db, email, user_obj.id)
    if otp_sent:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "OTP sent to your email, please verify your email to continue",
            },
        )

    db.close()


@user_router.post("/change-password")
async def change_password(
    data: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    old_password = data.old_password
    new_password = data.new_password
    user_obj = crud.user.get_by_email(db, email=current_user.email)
    if not user_obj:
        db.close()
        raise HTTPException(400, "User not found.")

    if old_password == new_password:
        db.close()
        raise HTTPException(400, "Old password and new password are same.")

    if not verify_password(old_password, user_obj.hashed_password):
        db.close()
        raise HTTPException(400, "Old password is incorrect.")

    hashed_password = get_password_hash(new_password)
    user_obj = crud.user.update(
        db, db_obj=user_obj, obj_in=schemas.UserUpdate(hashed_password=hashed_password)
    )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_DELTA)
    access_token = create_access_token(
        data={"sub": user_obj.email, "id": user_obj.id},
        expires_delta=access_token_expires,
    )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Password changed successfully.",
            "data": {"token": access_token, "token_type": "bearer"},
        },
    )


@user_router.post("/forgot-password")
async def forgot_password(data: schemas.EmailSchema, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    user_obj = crud.user.get_by_email(db, email=email)
    if not user_obj:
        db.close()
        raise HTTPException(400, "User not found.")

    otp_sent = await validate_email_send_otp(db, email, user_obj.id)
    if otp_sent:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "OTP sent to your email, please verify your email to continue",
            },
        )

    db.close()


@user_router.post("/reset-password")
async def reset_password(data: schemas.ResetPassword, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    otp_sent = data.otp.lower().strip()
    new_password = data.new_password

    email_otp_obj = crud.email_otp.get_by_email(db, email=email)
    user_obj = crud.user.get_by_email(db, email=email)
    if not email_otp_obj:
        db.close()
        raise HTTPException(400, "First proceed via sending OTP request.")

    otp = email_otp_obj.otp
    time_now = datetime.utcnow()

    if (((time_now - email_otp_obj.updated_at).total_seconds()) / 60) < 10:
        if str(otp_sent) == str(otp):
            hashed_password = get_password_hash(new_password)
            if verify_password(new_password, user_obj.hashed_password):
                db.close()
                raise HTTPException(400, "New password is same as your old password.")

            user_obj = crud.user.update(
                db,
                db_obj=user_obj,
                obj_in=schemas.UserUpdate(hashed_password=hashed_password),
            )
            hashed_password = get_password_hash(new_password)

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
        raise HTTPException(400, "OTP is expired, please proceed with new OTP.")


@user_router.post("/update-profile")
async def update_profile(
    data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_obj = crud.user.get_by_email(db, email=current_user.email)
    if not user_obj:
        db.close()
        raise HTTPException(400, "User not found.")

    user_obj = crud.user.update(db, db_obj=user_obj, obj_in=data)
    db.close()
    return JSONResponse(
        status_code=200,
        content={"success": True, "message": "Profile updated successfully."},
    )
