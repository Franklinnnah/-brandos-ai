from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_waitlist_table, add_to_waitlist

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WaitlistEntry(BaseModel):
    email: EmailStr

@app.on_event("startup")
def on_startup():
    create_waitlist_table()

@app.get("/")
def read_root():
    return {"Hello": "BrandOS.AI API"}

@app.post("/api/waitlist")
def join_waitlist(entry: WaitlistEntry):
    new_entry = add_to_waitlist(entry.email)
    if new_entry is None:
        raise HTTPException(status_code=409, detail="Email already on the waitlist.")
    return new_entry
