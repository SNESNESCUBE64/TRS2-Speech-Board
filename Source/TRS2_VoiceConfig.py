import board
import digitalio
import time
import audiomp3
import audiopwmio

ENGINE_TROUBLE_DELAY = [2, 30, 60, 0] #delay in tenth of a second
                      

class SoundDatabus:
    d0 = digitalio.DigitalInOut(board.GP12)
    d1 = digitalio.DigitalInOut(board.GP20)
    d2 = digitalio.DigitalInOut(board.GP13)
    d3 = digitalio.DigitalInOut(board.GP18)
    d4 = digitalio.DigitalInOut(board.GP19)
    ack = digitalio.DigitalInOut(board.GP21)
    
    voiceState = 0
    engineTroubleState = False
    
    def init(self):
        self.d0.direction = digitalio.Direction.INPUT
        self.d1.direction = digitalio.Direction.INPUT
        self.d2.direction = digitalio.Direction.INPUT
        self.d3.direction = digitalio.Direction.INPUT
        self.d4.direction = digitalio.Direction.INPUT
        self.ack.direction = digitalio.Direction.OUTPUT
        
        self.ack.value = True
    
    def updateVoiceState(self):
        self.voiceState = self.d0.value
        self.voiceState += self.d1.value * 2
        self.voiceState += self.d2.value *4
        self.voiceState += self.d3.value *8
        self.engineTroubleState = not self.d4.value

class VoiceSettings:
    dipsw0 = digitalio.DigitalInOut(board.GP0)
    dipsw1 = digitalio.DigitalInOut(board.GP1)
    dipsw2 = digitalio.DigitalInOut(board.GP2)
    dipsw3 = digitalio.DigitalInOut(board.GP3)
    dipsw4 = digitalio.DigitalInOut(board.GP4)
    dipsw5 = digitalio.DigitalInOut(board.GP5)
    dipsw6 = digitalio.DigitalInOut(board.GP6)
    dipsw7 = digitalio.DigitalInOut(board.GP7)
    
    muted = False
    startupSound = 0
    expEnable = False
    speechSet = 0
    engineTroubleDelay = 2
    
    def init(self):
        self.dipsw0.direction = digitalio.Direction.INPUT
        self.dipsw1.direction = digitalio.Direction.INPUT
        self.dipsw2.direction = digitalio.Direction.INPUT
        self.dipsw3.direction = digitalio.Direction.INPUT
        self.dipsw4.direction = digitalio.Direction.INPUT
        self.dipsw5.direction = digitalio.Direction.INPUT
        self.dipsw6.direction = digitalio.Direction.INPUT
        self.dipsw7.direction = digitalio.Direction.INPUT
        
    def readDipSwitches(self):
        self.muted = not self.dipsw0.value
        self.speechSet = (not self.dipsw1.value) * 2 + (not self.dipsw2.value)
        self.startupSound = (not self.dipsw3.value) * 2 + (not self.dipsw4.value)
        self.engineTroubleDelay = ENGINE_TROUBLE_DELAY[(not self.dipsw5.value) * 2 + (not self.dipsw6.value)]
        self.expEnable = not self.dipsw7.value
    


    
