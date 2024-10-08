import uuid
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware

from inference import predict

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to ECG Intelligence"}


@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    # Validate the file format
    if file.content_type != "image/hdf5":
        return {"error": "Invalid file format. Only HDF5 files are allowed."}

    # Process the file as needed
    prediction = await predict(file)  # Assuming prediction function is async
    return prediction
