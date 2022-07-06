#!/usr/bin/env python3
# Default used libs
from distutils.command.build import build
import os, sys, io, re, json, time

from requests import head
# Custom modules
from db import DB
from mac import Mac
from discovery import Discovery
# FastAPI
import uvicorn
from datetime import datetime, timedelta
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# openssl rand -hex 32
SECRET_KEY = "76d73f77e971926b8f31afd4dcfe911873f3164e1b600d7dd300ae9eeef0a68c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

fake_users_db = {
    "netmon": {
        "username":  "netmon",
        "full_name": "Netmon User",
        "telegram":  "123456789",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
        "admin": True
    }
}



app = FastAPI(
    title="Netmon",
    description="Netmon API endpoint"
)
db = DB()
mac = Mac()
ds = Discovery()

db.setDiscovery(ds)
ds.setMac(mac)
db.setMac(mac)

interface = "\\Device\\NPF_{FE303E25-2DBF-477A-87B6-891B3279AA74}"


# Set CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:443",
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None
    telegram: Union[str, None] = None


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(fdb, username: str):
    if username in fdb:
        user_dict = fdb[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/api/auth/token", response_model=Token)
async def login_for_access_token(response:Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=403, 
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # response.set_cookie(key="netmon_session", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/renew", response_model=Token)
async def renew_access_token(current_user: User = Depends(get_current_active_user)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=User)
async def auth_get_me(current_user: User = Depends(get_current_active_user)):
    return current_user



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/ping")
async def root():
    return {"ping": time.time()}


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

if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1', port=8000, reload=True, debug=True, workers=3)