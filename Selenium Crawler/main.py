import login
import api_requester
import class_id_grabber
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# ThreadPoolExecutor to manage concurrent Selenium sessions
executor = ThreadPoolExecutor(max_workers=5)  # Adjust max_workers based on your system's capacity

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with the specific frontend URL for security, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define input model
class ClassRequest(BaseModel):
    username: str
    password: str
    class_name: str
    section: int

def run_selenium(username, password, classInfo):
    """
    Function to run the Selenium process in a separate thread.
    """
    try:
        # Call the existing function
        return class_id_grabber.get_all_info(username, password, classInfo)
    except Exception as e:
        raise RuntimeError(f"Error in Selenium execution: {e}")

@app.post("/get_class_data/")
async def get_class_data(request: ClassRequest):
    try:
        # Prepare classInfo for get_all_info
        classInfo = [request.class_name, request.section]

        # Run Selenium in a separate thread
        future = executor.submit(run_selenium, request.username, request.password, classInfo)
        classdata = future.result()  # Wait for the thread to complete and get the result

        classdata_dict = {
            "class_name": classdata[0],
            "available_seats": classdata[1],
            "instructors": classdata[2],
            "schedule": classdata[3],
        }
        return {"classdata": classdata_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))