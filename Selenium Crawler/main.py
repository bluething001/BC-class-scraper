import login
import api_requester
import class_id_grabber
import tkinter as tk
from tkinter import messagebox
import threading
import random
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import class_id_grabber

app = FastAPI()

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

@app.post("/get_class_data/")
async def get_class_data(request: ClassRequest):
    try:
        # Prepare classInfo for get_all_info
        classInfo = [request.class_name, request.section]
        # Call the existing function
        classdata = class_id_grabber.get_all_info(request.username, request.password, classInfo)
        classdata_dict = {
            "class_name": classdata[0],
            "available_seats": classdata[1],
            "instructors": classdata[2],
            "schedule": classdata[3],
        }
        return {"classdata": classdata_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# def random_sleep_time():
#     return random.random() * 1.0 + 2.0

# classInfo = ["PHYS2201 Introductory Physics II (Calculus)", 1]

# classdata = class_id_grabber.get_all_info("guoale", "j2dhdgt7", classInfo)
# print(classdata)