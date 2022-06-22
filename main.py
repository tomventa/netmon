import os, sys, io, re, json, time
from tkinter.messagebox import RETRY
from fastapi import FastAPI
from db import DB
from mac import Mac
from discovery import Discovery

app = FastAPI()
db = DB()
mac = Mac()
ds = Discovery()

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
    return {"devices": db.getDevices()}

@app.get("/api/scan")
async def scan():
    """Scan the network and return a list of devices

    Returns:
        json: A complete json list of devices
    """
    result = ds.scan(interface)
    db.autoInsert(result)
    db.updateDevices(result)
    return {"message": "Scanning the network...", "result": result}

@app.get("/api/lastScan")
async def lastScan():
    return {"lastScan": 0}