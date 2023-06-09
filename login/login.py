import azure.functions as func

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt

import os

app = FastAPI()

# In-memory storage for simplicity
users = [
    {"username": "alice", "password": "password1"},
    {"username": "bob", "password": "password2"},
]

# Secret key for signing and verifying tokens
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token generation and verification functions
def generate_token(username: str):
    # Set the token expiration time
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    # Create the JWT token
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class User(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(form_data: User):
    username = form_data.username
    password = form_data.password

    for user in users:
        if user["username"] == username and user["password"] == password:
            token = generate_token(username)
            return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid username or password")

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)
