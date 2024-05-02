import time
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


from recipe_assistant.routers import users, chat
from recipe_assistant.utils.db import DatabaseStore
from recipe_assistant.utils.openai_client import OpenAIClient
from recipe_assistant.utils.cache import InMemoryCache
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://0.0.0.0:5173",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8080",
    "https://recipe-agent-frontend.greenmeadow-35e3d21d.westus3.azurecontainerapps.io"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseStore.startup()
    OpenAIClient.startup()
    InMemoryCache.startup()
    yield
    await DatabaseStore.shutdown()
    OpenAIClient.shutdown()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(users.router)
app.include_router(chat.router)


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
