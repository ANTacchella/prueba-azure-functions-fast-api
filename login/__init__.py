import azure.functions as func

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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

    # Return the token
    return {"access_token": 123}


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)
