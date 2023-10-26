from fastapi import FastAPI
import sys
import time
from ctypes import *
from contextlib import asynccontextmanager
from routes import digital_discovery
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(appliaction: FastAPI):
    try:
        """connects to Discovery board and trys to configure it"""
        appliaction.state.dwf = cdll.LoadLibrary("libdwf.so")
        appliaction.state.hdwf = c_int()
        appliaction.state.dwf.FDwfDeviceOpen(c_int(-1),byref(appliaction.state.hdwf))
        appliaction.state.dwf.FDwfDeviceAutoConfigureSet(appliaction.state.hdwf,c_bool(1))
        appliaction.state.dwf.FDwfDeviceReset(appliaction.state.hdwf)
    except Exception:
        raise Exception
    yield
    appliaction.state.dwf.FDwfDeviceCloseAll()


app = FastAPI(separate_input_output_schemas= False, lifespan=lifespan)
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(digital_discovery.router)
