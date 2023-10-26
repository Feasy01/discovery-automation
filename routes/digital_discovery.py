from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status, Request
import os
import time
from ctypes import *
from models.I2C_Configuration import I2cConfiguration
from models.CAN_Configuration import CANConfiguration
router = APIRouter(
    prefix="/digital_discovery",
    tags=["digital_discovery"]
)
@router.post("/config")
def configure_digigtal_discovery(request:Request)-> None :
    print(os.getcwd())
    print (request.app.state.siema)
    return request.app.state.siema
    return "witam"
    pass

@router.post("/I2C_read", status_code=status.HTTP_200_OK)
def read_i2c(request:Request, device:I2cConfiguration) -> []:
    request.app.state.hdwf
    iNak = c_int()
    request.app.state.dwf.FDwfDigitalI2cRateSet(request.app.state.hdwf,c_double(device.data_rate))
    request.app.state.dwf.FDwfDigitalI2cSclSet(request.app.state.hdwf, c_int(device.scl_pin)) # SCL = DIO-0
    request.app.state.dwf.FDwfDigitalI2cSdaSet(request.app.state.hdwf, c_int(device.sda_pin)) # SDA = DIO-1
    request.app.state.dwf.FDwfDigitalI2cClear(request.app.state.hdwf, byref(iNak))
    if iNak.value == 0:
        print("I2C bus error. Check the pull-ups.")
        raise HTTPException(status_code=400, detail="I2C bus error. Check the pull-ups.")
    time.sleep(1)
    rgRX = (c_ubyte*device.bytes_to_read)()
    request.app.state.dwf.FDwfDigitalI2cRead(request.app.state.hdwf, c_int(device.adr8bits<<1), rgRX, c_int(device.bytes_to_read), byref(iNak))
    return list(rgRX)

@router.post("/CAN_read",status_code=status.HTTP_200_OK)
def read_can(request:Request, device:CANConfiguration):
    request.app.state.dwf.FDwfDigitalCanRateSet(request.app.state.hdwf, c_double(device.data_rate)) # 1MHz
    request.app.state.dwf.FDwfDigitalCanPolaritySet(request.app.state.hdwf, c_int(0)) # normal
    request.app.state.dwf.FDwfDigitalCanTxSet(request.app.state.hdwf, c_int(device.tx_pin)) # TX = DIO-0
    request.app.state.dwf.FDwfDigitalCanRxSet(request.app.state.hdwf, c_int(device.rx_pin)) # RX = DIO-1

    rgbTX = (c_ubyte*4)(0,1,2,3)
    vID  = c_int()
    fExtended  = c_int()
    fRemote  = c_int()
    cDLC = c_int()
    vStatus  = c_int()
    rgbRX = (c_ubyte*device.can_bytes_to_receive)()
    request.app.state.dwf.FDwfDigitalCanRx(request.app.state.hdwf, None, None, None, None, None, c_int(0), None) # initialize RX reception
    time.sleep(1)
    tsec = time.clock() + device.can_time_to_scan
    while time.cloc() < tsec:
        time.sleep(0.01)
        request.app.state.dwf.FDwfDigitalCanRx(request.app.statehdwf, byref(vID), byref(fExtended), byref(fRemote), byref(cDLC), rgbRX, c_int(sizeof(rgbRX)), byref(vStatus)) 
        if vStatus.value != 0:
            print("RX: "+('0x{:08x}'.format(vID.value)) +" "+("Extended " if fExtended.value!=0 else "")+("Remote " if fRemote.value!=0 else "")+"DLC: "+str(cDLC.value))
            if vStatus.value == 1:
                print("no error")
            elif vStatus.value == 2:
                print("bit stuffing error")
            elif vStatus.value == 3:
                print("CRC error")
            else:
                print("error")
            if fRemote.value == 0 and cDLC.value != 0:
                print("Data: "+(" ".join("0x{:02x}".format(c) for c in rgbRX[0:cDLC.value])))


    #TODO DATA ACUMULATION
    return("zakonczono")



    

