from FakeDevices import *
import logging

log = logging.getLogger(__name__)

# Modify only the code between try-except. Please leave the rest
# as it is.
try:
    gui = Gui()
    # DHT -- temperature and humdity sensor is connected to D6.
    # You can have more than 1 DHT by adding more.
    gui.add(DHT(4, 'Room'))
    # Add your main Python program here. My example here is "main",
    # yours might be a different name. Please change accordingly.    
    from smart_temp_controller import *
except:
    # Generate exception traceback to help debugging
    log.exception('----------------Log----------------')
    
# Make sure to call gui.quit(). Otherwise the GUI will not be closed
# after the program terminated.
gui.quit()
# Inform the user that the program has terminated
print('Program terminated.')

