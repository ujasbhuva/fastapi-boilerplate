import random
from datetime import datetime

from fastapi import HTTPException

from server import crud, schemas
from server.utils.mail import send_email


async def validate_email_send_otp(db, email, user_id):
    time_now = datetime.utcnow()
    key = random.randint(99999, 999999)
    old_otp_obj = crud.email_otp.get_by_email(db, email=email)
    if old_otp_obj:
        attempts = old_otp_obj.attempts
        if (attempts >= 10) and (
            (((time_now - old_otp_obj.updated_at).total_seconds()) / 3600) > 24
        ):
            crud.email_otp.update(
                db,
                db_obj=old_otp_obj,
                obj_in=schemas.EmailOtpUpdate(created_at=time_now, attempts=1),
            )
            await send_email(email, key)
            return True
        if (attempts >= 10) and (
            (((old_otp_obj.updated_at - old_otp_obj.created_at).total_seconds()) / 60)
            < 10
        ):
            raise HTTPException(429, "Sending otp limit exceeded. try after 24 hours")
        if attempts >= 10:
            raise HTTPException(429, "Sending otp limit exceeded. try after sometime")
        crud.email_otp.update(
            db,
            db_obj=old_otp_obj,
            obj_in=schemas.EmailOtpUpdate(
                created_at=time_now, attempts=old_otp_obj.attempts + 1, otp=key
            ),
        )
    else:
        crud.email_otp.create(
            db,
            obj_in=schemas.EmailOtpBase(
                email=email, attempts=1, otp=key, user_id=user_id
            ),
        )
    await send_email(email, key)
    return True
