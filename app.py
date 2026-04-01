import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from pymongo import MongoClient
from pymongo.errors import PyMongoError


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "codex_app")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "submissions")

app = FastAPI(title="Submission Form App")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Submission(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)


def get_collection():
    if not MONGODB_URI:
        raise HTTPException(
            status_code=500,
            detail="MongoDB is not configured. Set the MONGODB_URI environment variable.",
        )

    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    database = client[MONGODB_DB]
    return database[MONGODB_COLLECTION]


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = BASE_DIR / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.post("/api/submissions")
async def create_submission(submission: Submission):
    try:
        collection = get_collection()
        result = collection.insert_one(submission.model_dump())
    except HTTPException:
        raise
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc

    return {
        "message": "Submission saved successfully.",
        "id": str(result.inserted_id),
    }
