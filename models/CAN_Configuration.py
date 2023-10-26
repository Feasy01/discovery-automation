from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class CANConfiguration(BaseModel):
    tx_pin : int  = os.getenv("TX_PIN");
    rx_pin : int = os.getenv("RX_PIN");
    data_rate : int = os.getenv("CAN_DEFAULT_RATE");
    can_time_to_scan : int = os.getenv("CAN_TIME_TO_SCAN");
    can_bytes_to_receive : int = os.getenv("CAN_BYTES_TO_RECEIVE");