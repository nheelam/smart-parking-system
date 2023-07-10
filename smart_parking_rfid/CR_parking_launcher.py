from FakeDevices import *
import logging

log = logging.getLogger(__name__)

try:
    gui = Gui()
     
    #RFID
    gui.add(MifareRfid('test2.json'))
    
    # ultrasonic
    gui.add(Ultrasonic(9, 'Car distance from parking slot 1 (m)'))
    gui.add(Ultrasonic(13, 'Car distance from parking slot 2 (m)'))

            

   

    from CR_parking import *
except:
    log.exception('----------------Log----------------')
    

gui.quit()
print('Program terminated.')

