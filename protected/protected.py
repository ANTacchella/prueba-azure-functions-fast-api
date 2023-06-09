import azure.functions as func

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import os

app = FastAPI()

# Secret key for signing and verifying tokens
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        return username
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Logic for the protected route
    return {"message": f"Welcome, {username}! You are authorized to access this route!"}

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)
