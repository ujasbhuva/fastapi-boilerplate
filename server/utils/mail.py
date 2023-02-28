from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from server.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def get_signup_template(otp):
    return f"""<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                <div style="margin:20px auto;width:1000px;padding:20px 0">
                    <div style="border-bottom:1px solid #eee">
                    <a href="" style="font-size:1.5rem;color: #00466a;text-decoration:none;font-weight:600">FastAPI Boilerplate</a>
                    </div>
                    <p style="font-size:1.1em">Hi there,</p>
                    <p>Thank you for choosing FastAPI Boilerplate. Use the following OTP to complete your Sign Up process. OTP is valid for 10 minutes</p>
                    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
                    <p style="font-size:0.9em;">Regards,<br />FastAPI Boilerplate</p>
                    <hr style="border:none;border-top:1px solid #eee" />
                    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                    <p>FastAPI Boilerplate. Inc</p>
                    <p>1600 Amphitheatre Parkway</p>
                    <p>California</p>
                    </div>
                </div>
                </div>
            """


async def send_email(email, otp):
    message = MessageSchema(
        subject="OTP for email verification",
        recipients=[email],
        body=get_signup_template(otp),
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return True
