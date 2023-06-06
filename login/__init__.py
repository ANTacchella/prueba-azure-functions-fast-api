import azure.functions as func

from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# Create an OAuth2PasswordBearer security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Define a user model
class User(BaseModel):
    username: str
    password: str

# Define a login endpoint
@app.post("/login")
async def login(user: User):
    # Check if the user exists in the database
    if not user.username == "Azure":
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check if the user's password is correct
    if not user.password == "Azure":
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create a token for the user
    token = oauth2_scheme.create_access_token(user.username)

    # Return the token
    return {"access_token": token}


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)
