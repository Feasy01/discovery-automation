from pydantic import BaseModel
import os
from dotenv import load_dotenv
from ctypes import *
load_dotenv()

class I2cConfiguration(BaseModel):
    sda_pin : int  = int(os.getenv("SDA_PIN"));
    scl_pin : int = int(os.getenv("SCL_PIN"));
    data_rate : int = int(os.getenv("I2C_DEFAULT_RATE"));
    adr8bits: bytes = c_byte(int(os.getenv("I2C_DEFAULT_ADR")));
    bytes_to_read : int = int(os.getenv("I2C_DEFAULT_BYTES_TO_RECEIVE"));