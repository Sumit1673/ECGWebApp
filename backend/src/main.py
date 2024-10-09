import logging
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inference import predict

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


app = FastAPI()

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a Pydantic model for request body validation
class UserData(BaseModel):
    username: str
    email: str


@app.get("/")
def read_root():
    return {"message": "Welcome to ECG Intelligence"}


@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    
    contents = await file.read()
    return predict(contents)


# Define the POST route
@app.post("/test")
async def submit_data(user_data: UserData):
    # Return the received data as a JSON response
    return {
        "message": "Data received successfully",
        "data": {
            "username": user_data.username,
            "email": user_data.email
        }
    }
