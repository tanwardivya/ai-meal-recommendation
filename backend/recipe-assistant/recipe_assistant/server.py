import time
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio

from recipe_assistant.routers import users

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_CONNECTION_STRING"))
db = client.agent
user_collection = db.get_collection("users")



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    return {"message": "Recipe Assistant"}
