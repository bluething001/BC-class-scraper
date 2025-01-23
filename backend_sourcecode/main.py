from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define request schema using Pydantic
class StartScraperRequest(BaseModel):
    username: str
    password: str

# Define endpoints
@app.post("/api/start")
async def start_scraper(request: StartScraperRequest):
    # Extract username and password
    username = request.username
    password = request.password
    # Start the scraper (mocked)
    return {"message": f"Scraper started for user {username}!"}

@app.post("/api/stop")
async def stop_scraper():
    # Stop the scraper (mocked)
    return {"message": "Scraper stopped!"}