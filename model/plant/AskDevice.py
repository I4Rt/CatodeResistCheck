class AskDevice:
    
    READ_BYTE = b'\x01'
    
    def __init__(self, recId:bytes, devId:bytes) -> None:
        self._recId = recId
        self._devId = devId
        