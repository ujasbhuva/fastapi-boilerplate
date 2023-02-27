# FastAPI - boilerplate with authentication

## Run Development Server Locally


create virtual environment
```
python -m venv venv
```

activate environment
```
source venv/bin/activate
```

install dependencies
```
pip install -r requirements.txt
```
(*you may need to reinstall dependencied for fastapi-mail, bcrypt and starlette (**use: pip install fastapi-mail bcrypt starlette==0.22.0**)*)

start server locally
```
uvicorn server.main:app --reload --port 8013
```
