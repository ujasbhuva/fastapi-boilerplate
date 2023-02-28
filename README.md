# FastAPI - Auth Boilerplate
Boilerplate with User Authentication Operations, SQLAlchemy, Alembic, Pydantic, and JWT

Auth functions:
- User sign up with otp
- User login
- Update profile
- Forgot password with otp verification
- Change password

#


## Start Development Server


Create virtual environment
```
python -m venv venv
```


Activate environment
```
source venv/bin/activate
```


Install dependencies (*you may need to reinstall dependencied for fastapi-mail, bcrypt and starlette (**use: pip install fastapi-mail bcrypt starlette==0.22.0**)*)
```
pip install -r requirements.txt
```



Database migration (*this project currently uses sqlite to manage the database, you can use any sql by changing database connection string at `SQLALCHEMY_DATABASE_URI` in .env file*)
```
python migrate_db.py
```



Start server
```
uvicorn server.main:app --reload --port 8013
```
