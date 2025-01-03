from model.plant.AskDevice import AskDevice
from tools.AskInterfaceTool import *
from serial import Serial
class MeasuringDeviceLogic(AskDevice):
    
    def __init__(self, recId: bytes, devId: bytes) -> None:
        super().__init__(recId, devId)
        self.deviceType = b'\x06'
        
    def readData(self, ser: Serial):
        '''
        returns:
            res:     bool
            code:    int
            voltage: int
            resist:  int
            
        codes:
             0,  'Нормальный ответ, парсинг выполнен'
            -1,  'Слишкий малый размер ответа'
            -2,  'Слишкий большой размер ответа'
            -3,  'Ошибка в сообщении'
            -4,  'Неизвестная форма овтета'
            -5,  'Ответ несовпадает запрашиваемым ID устрйоства'
        '''
        message = self._recId + self._devId + self.READ_BYTE + self.deviceType
        size, answer = sendMessage(ser, message)
        res, code, voltage, resist =  self.parseAnswer(size, answer)
        return res, code, voltage, resist
        
        
        
    
    def parseAnswer(self, size:int, answer:bytes) -> tuple[bool, int, float|None, int|None]:
        '''
        returns:
            res:     bool
            code:    int
            voltage: float
            resist:  int
            
        codes:
             2,  'Нормальный ответ, парсинг выполнен, выявленно КЗ'
             1,  'Нормальный ответ, парсинг выполнен, выявлен обрыв'
             0,  'Нормальный ответ, парсинг выполнен'
            -1,  'Слишкий малый размер ответа'
            -2,  'Слишкий большой размер ответа'
            -3,  'Ошибка в сообщении'
            -4,  'Неизвестная форма овтета'
            -5,  'Ответ несовпадает запрашиваемым ID устрйоства'
        '''
        if self._recId == answer[0:1] and self._devId == answer[1:2]:
            if size < 11:
                return False, -1, None, None
            res, code, msg =  checkAnswer(size, answer)
            if res:
                voltage = hexToInt(answer[5:7])/10
                resist  = hexToInt(answer[7:9])
                
                
                if answer[7:9] == b'\xff\xff':
                    return True, 1, voltage, resist # Обрыв
                elif answer[7:9] == b'\x00\x00':
                    return True, 2, voltage, resist # КЗ
                return True, 0, voltage, resist
            return False, code, None, None
        return False, -5, None, None
        
    
    
