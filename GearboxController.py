"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Gearbox Controller.

"""

from Gearbox import Gearbox

import subprocess
import urllib.request
import time
import sys

class GearboxController():
    """Class containing the Gearbox Controller for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model
        self.instrument = Gearbox()
        
    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def Start_Server(self, gearbox, image):
    #This methods opens a Gearbox server at local host port:2950 and create a session with the selected image
        sys.stdout("\nTrying to open Gearbox Server...\n")
        cmd = "C:\\toolsuites\\gearbox\\gearboxj\\" + gearbox + "\\gearboxj server -s http://localhost:2950"
        tempBatch = open("Configuration/gearbox.bat", 'w')
        tempBatch.write(cmd)
        tempBatch.close()
        subprocess.Popen("Configuration\gearbox.bat", shell=True)
        test = urllib.request.urlopen('http://localhost:2950///general.createAuroraSession?name=temp&modelFile=' + image, timeout=120).read().decode('UTF-8')
        
        if test[:2] == "OK":
            sys.stdout("\nGearbox Server opened on port 2950\n")
            return(True)
        else:
            sys.stdout(test)
            return(False)
        
    def Stop_Server(self, args=[]):
    #This method closes the Gearbox Server at local host port:2950
        urllib.request.urlopen('http://localhost:2950/plain/manager/general.cleanupServer')
        urllib.request.urlopen('http://localhost:2950///general.shutdownServer')
        sys.stdout('\nServer connection is closed.\n')

#####################################################################################################################################################################################################################################################################################
        
    def Open_connection(self):
        urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/general.createConnection?name=left&medium=HiPro&side=Left&protocol=PIF2FW&connected=true') 
        
    def Close_connection(self):
        urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/general.removeConnection?connection=manager/sessions/temp/connections/left') #Lukker en Connection til device
        sys.stdout('\nHiPro connection is closed.\n')

#####################################################################################################################################################################################################################################################################################
        
    def Read_device_info(self, args=[]):
        try:
            info = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.readDeviceInfo').read()  #Read Device info
            info = info.decode(encoding='UTF-8')
            info = info.split('readDeviceInfo')    #Gearbox returns the data as bytes. This line change the 'bytes' to 'string'
            sys.stdout(info)

        except:
            self.view.view.sendError("604", "Gearbox ERROR")
            return("ERROR")

    def Read_identity(self, args=[]):
        try:
            identity = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.identifyDevice').read()  #Read Indentify device
            identity = identity.decode(encoding='UTF-8').split('identifyDevice')[1]    #Gearbox returns the data as bytes. This line change the 'bytes' to 'string'
            sys.stdout(identity)

        except:
            self.view.view.sendError("605", "Gearbox ERROR")
            return("ERROR")
    
    def Read_serial_number(self, args=[]):
        try:
            serial = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.readSerialNumber').read()    #Read Serial number
            serial = serial.decode(encoding='UTF-8').split('readSerialNumber')[1]
            sys.stdout(serial)

        except:
            self.view.view.sendError("603", "Gearbox ERROR")
            return("ERROR")
    
    def Identify_FE_chip(self, args=[]):
        try:
            serial = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.identifyFE').read()    #Read Serial number
            serial = serial.decode(encoding='UTF-8').split('identifyFE')[1]
            self.instrument.measure["Identify_FE"] = [list(serial)]
            sys.stdout(serial)

        except:
            self.view.view.sendError("600", "Gearbox ERROR")
            return("ERROR")
    
    def Identify_DSP_chip(self, args=[]):
        try:
            serial = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.identifyDSP').read()    #Read Serial number
            serial = serial.decode(encoding='UTF-8').split('identifyDSP')[1]
            self.instrument.measure["Identify_DSP"] = [list(serial)]
            sys.stdout(serial)

        except:
            self.view.view.sendError("601", "Gearbox ERROR")
            return("ERROR")
    
    def Identify_RF_chip(self, args=[]):
        try:
            serial = urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/general.identifyRF').read()    #Read Serial number
            serial = serial.decode(encoding='UTF-8').split('identifyRF')[1]
            self.instrument.measure["Identify_RF"] = [list(serial)]
            sys.stdout(serial)

        except:
            self.view.view.sendError("602", "Gearbox ERROR")
            return("ERROR")

#####################################################################################################################################################################################################################################################################################
        
    def EAS_set_generator_output(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/productionTest.signalGenerators.configureOutputSignalGenerator?newToneFrequency='+str(args[0])+'&newGain='+ str(args[7])[-1] +'&enable='+str(args[8])
            url = url.replace(" ", "%20")
            urllib.request.urlopen(url).read() 
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("602", "Gearbox ERROR")
            return("ERROR")

#####################################################################################################################################################################################################################################################################################
            
    def BLE_DTM_StartTX(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/nwt.dtmStartTxTest?frequency=' + str(args[7]) + '&data_length=' + str(args[0]) + '&payload_type=' + str(args[8])
            url = url.replace(" ", "%20")
            serial = urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8').split('dtmStartTxTest')[1]
            sys.stdout(serial)

        except:
            self.view.view.sendError("606", "Gearbox ERROR")
            return("ERROR")

    def BLE_DTM_StartRX(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/nwt.dtmStartRxTest?frequency=' + str(args[7])
            url = url.replace(" ", "%20")
            urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8').split('dtmStartRxTest')[1]
            sys.stdout(serial)

        except:
            self.view.view.sendError("607", "Gearbox ERROR")
            return("ERROR")

    def BLE_DTM_EndTest(self, args=[]):
        try:
            urllib.request.urlopen('http://localhost:2950//manager/sessions/temp/connections/left/nwt.dtmEndTest').read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("608", "Gearbox ERROR")
            return("ERROR")

#####################################################################################################################################################################################################################################################################################

    def init_XP(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/medicalTests.medicalTests.Initialization?clock_out_activation=Activate&DC_DC=Enable&VHF=' + str(args[7]) + '&output_mux=OOK&carrier_frequency=' + str(args[0]) + '&divisor=32&duty_cycle=' + str(args[1]) + '&med_drv_a_cfg=tx_data&med_drv_b_cfg=tx_data&xp_clock=0.974'
            url = url.replace(" ", "%20")
            serial = urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("609", "Gearbox ERROR")
            return("ERROR")
        
    def getID_XP(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/medicalTests.medicalTests.GetID?startup_precharges=100&Precharge=1920&manchester_speed=32&Frame_Interval=24000&Capture_Type=GPIO'
            url = url.replace(" ", "%20")
            serial = urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("610", "Gearbox ERROR")
            return("ERROR")
        
    def getClock_XP(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/medicalTests.medicalTests.GetClock?startup_precharges=100&Precharge=1920&manchester_speed=32&Frame_Interval=24000&Capture_Type=GPIO'
            url = url.replace(" ", "%20")
            serial = urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("611", "Gearbox ERROR")
            return("ERROR")
        
    def getVunreg_XP(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/medicalTests.medicalTests.GetVunreg?Precharge=1920&Frame_Interval=24000&Capture_Type=ADC'
            url = url.replace(" ", "%20")
            serial = urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("612", "Gearbox ERROR")
            return("ERROR")
        
    def stopCMD(self, args=[]):
        try:
            url = 'http://localhost:2950//manager/sessions/temp/connections/left/medicalTests.medicalTests.STOP'
            url = url.replace(" ", "%20")
            urllib.request.urlopen(url).read()
            serial = serial.decode(encoding='UTF-8')
            sys.stdout(serial)

        except:
            self.view.view.sendError("613", "Gearbox ERROR")
            return("ERROR")
        

#####################################################################################################################################################################################################################################################################################

    def Custom(self, args=[]):
        try:
            url = args[0]
            url = url.replace(" ", "%20")
            urllib.request.urlopen(url)

        except:
            self.view.view.sendError("698", "Gearbox ERROR")
            return("ERROR")

    def CustomRead(self, args=[]):
        try:
            url = args[0]
            url = url.replace(" ", "%20")
            urllib.request.urlopen(url).read()

        except:
            self.view.view.sendError("699", "Gearbox ERROR")
            return("ERROR")
        