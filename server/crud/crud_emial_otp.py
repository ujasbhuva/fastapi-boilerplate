from typing import List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from server.crud.base import CRUDBase
from server.models.user import EmailOtp
from server.schemas.email_otp import EmailOtpCreate, EmailOtpUpdate

UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDEmailOTP(CRUDBase[EmailOtp, EmailOtpCreate, EmailOtpUpdate]):
    def get_all(self, db: Session) -> List[EmailOtp]:
        return db.query(EmailOtp).all()

    def get_by_id(self, db: Session, *, id: str) -> EmailOtp:
        return db.query(EmailOtp).filter(EmailOtp.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> EmailOtp:
        return db.query(EmailOtp).filter(EmailOtp.email == email).first()

    def create(self, db: Session, *, obj_in: EmailOtpCreate) -> EmailOtp:
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: EmailOtp, obj_in: EmailOtpUpdate
    ) -> EmailOtp:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> Optional[EmailOtp]:
        return super().remove(db, id=id)


email_otp = CRUDEmailOTP(EmailOtp)
