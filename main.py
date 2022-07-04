import os, sys, io, re, json, time
from tkinter.messagebox import RETRY
from fastapi import FastAPI
import uvicorn
from db import DB
from mac import Mac
from discovery import Discovery
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db = DB()
mac = Mac()
ds = Discovery()

# Set CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.setDiscovery(ds)
ds.setMac(mac)
db.setMac(mac)

interface = "\\Device\\NPF_{FE303E25-2DBF-477A-87B6-891B3279AA74}"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/get/db")
async def getDB():
    return {"message": "DB is no ready yet"}

@app.get("/api/devices")
async def devices() -> list:
    """Get a list of devices currently connected

    Returns:
        list: _description_
    """
    return {"devices": db.getCurrentDevices()}

@app.get("/api/scan")
async def scan():
    """Scan the network and return a list of devices

    Returns:
        json: A complete json list of devices
    """
    result = ds.scan(interface)
    db.autoInsert(result)
    db.sync()
    return {"message": "Scanning the network...", "result": result}

@app.get("/api/lastScan")
async def lastScan():
    return {"lastScan": 0}

@app.get("/api/auth/me")
async def authme():
    return {"auth": True,
            "username": "user",
            "capitalize": True,
            "role": "admin",
            "essential": True,
            "since": 0}

if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1', port=8000, reload=True, debug=True, workers=3)