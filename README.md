# **ECG2AF WebApp**

Develop a web application that accurately predicts the **risk** of developing **atrial fibrillation (AF)** in individuals based on their **electrocardiogram (ECG)** data. The application will leverage a machine learning model trained on comprehensive ECG recordings and AF diagnosis datasets.

This project performs the following tasks:

1. Creates a UI interface using HTML.
2. Takes input as an ECG file, along with the user's name and email address.
3. Sends the request to the backend (FastAPI), where the file and processed and passed to the model for generating results.
4. Display the prediction result.

## Architecture Diagram 1
The image shown below explains the architecture followed to build this project.

![Basic Architecture](https://github.com/Sumit1673/ECGWebApp/blob/main/arch_images/arch1.png)


Front end utilizes docker with nginx as the base to forward the request to the backend to a port where fastapi is listening. Server reads the request and forward it to specific function for further processing.

The backend server and model are running on a docker that utilizes ***ML-Base*** as its base image. *ML-Base is custom-built image that avoids pulling the model using git-lfs from the base repository and handles model dependencies.
Model dependencies are taken from **ghcr.io/broadinstitute/ml4h:tf2.9-latest-cpu***. This image acts as base image for ML-Base. To further understand this have a look to the docker file inside [ml-base](https://github.com/Sumit1673/ECGWebApp/tree/main/ml-base)


In a real-world scenario model is saved in cloud storage(like S3/GCS) for easy access of the model.

### **Steps to run the code:**

1. Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) on your local.

1. Clone the repo
2. cd ECGWebApp
3. run the command: docker compose build --no-cache; docker compose up; docker compose down
4. goto http://localhost:8080/
5. Upload the image, enter your details (any random values). user details were added keeping in mind for future auditing and logging of the inputs.
6. Submit

## Architecture Diagram 2 (Scalable to multiple workloads)

![Scalable Architecture](https://github.com/Sumit1673/ECGWebApp/blob/main/arch_images/ECGWebAPP.png)

Changes will be made to the Arch 1 to deal with multiple users and batch data for processing.

1. **Load Balancer:** This will help in handling the excessive workload that comes in and passes this to the backend server whichever is available. Load balancer listens a users request from a particular port. When a request arrives, the load balancer typically uses the client's IP address as part of its decision-making process where it applies a hashing function to the client's IP address, generating a unique numerical value. This hash value is then used to select a backend server from a predefined list. 

2. **TF Serving:**  
  1. It is a powerful tool for deploying machine learning models in production environments. It offers high performance, scalability, and efficient handling of multiple model versions.
  2. TensorFlow Serving excels in resource management. No need have a seperate code for batch processing it automatically handles batching requests and optimizes memory usage.
  3.  Ref: https://www.tensorflow.org/tfx/guide/serving



**Libraries and Tools:** Python, TF, numpy

**Web FrameWork:** FastAPI

**FrontEnd:** HTML

**Containarization:** Docker and Docker-Compose

# Initial Thoughts:
I thought to create a devcontainer which will avoid using local machine and setting things up which can be hassle sometime.
But after building the code when i tested it, it was found that codespace has issue with [ports] (https://notes.alexkehayias.com/codespaces-doesn-t-allow-requests-across-ports-from-a-preview/).

So moved the project to local.
