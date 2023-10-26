from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class SPIConfiguration(BaseModel):
    dq0_mosi_siso_pin : int  = os.getenv("DQ0_MOSI_SISO_PIN");
    dq1_miso_pin : int = os.getenv("DQ1_MISO_PIN");
    data_rate : int = os.getenv("I2C_DEFAULT_RATE");
    adr8bits: bytes = os.getenv("I2C_DEFAULT_ADR");
    bytes_to_read : int = os.getenv("I2C_DEFAULT_BYTES_TO_READ");