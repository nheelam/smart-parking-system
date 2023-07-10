from FakeDevices import *
import logging

log = logging.getLogger(__name__)

try:
    gui = Gui()
    #RFID
    gui.add(MifareRfid('test2.json'))
   

    from testRfid2 import *
except:
    log.exception('----------------Log----------------')
    

gui.quit()
print('\nProgram terminated.')


