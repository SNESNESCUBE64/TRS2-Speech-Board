import board
import digitalio
import time

EXP_WAVE1_LAMP_MASK = 0x0001
EXP_WAVE2_LAMP_MASK = 0x0002
EXP_WAVE3_LAMP_MASK = 0x0004
EXP_ALPHA_LAMP_MASK = 0x0008
EXP_BRAVO_LAMP_MASK = 0x0010
EXP_CHARLIE_LAMP_MASK = 0x0020
EXP_CAUTION_LAMP_MASK = 0x0040
EXP_SUCCESS_LAMP_MASK = 0x0080
EXP_ENGINE_LAMP_MASK = 0x0100
EXP_GAMEOVER_LAMP_MASK = 0x0200
EXP_SCRAMBLE_MASK = 0x0400
EXP_STATE0_MASK = 0x0800
EXP_STATE1_MASK = 0x1000
EXP_STATE2_MASK = 0x2000
EXP_STATE3_MASK = 0x4000
EXP_COMM_MASK = 0x8000

GAME_OVER = 0
GAME_START = 1
BEEP = 2 #Not used
WAVE_COMPLETE = 3
WAVE_1_CHARLIE = 4
WAVE_1_BRAVO = 5
WAVE_1_ALPHA = 6
WAVE_1_CAUTION = 7
WAVE_2_CHARLIE = 8
WAVE_2_BRAVO = 9
WAVE_2_ALPHA = 10
WAVE_2_CAUTION = 11
WAVE_3_CHARLIE = 12
WAVE_3_BRAVO = 13
WAVE_3_ALPHA = 14
WAVE_3_CAUTION = 15


class ExpDriver:
    expData = digitalio.DigitalInOut(board.GP28) 
    expLatch = digitalio.DigitalInOut(board.GP27) 
    expClock = digitalio.DigitalInOut(board.GP8)
    expClear = digitalio.DigitalInOut(board.GP26)
    expCS1 = digitalio.DigitalInOut(board.GP9)
    expCS2 = digitalio.DigitalInOut(board.GP10)
    expCS3 = digitalio.DigitalInOut(board.GP22)
    expAck = digitalio.DigitalInOut(board.GP11)
    
    expLampState = 0xFFFF
    expEnable = False
    
    def init(self, enable):
        self.expEnable = enable
        if enable:
            self.expData.direction = digitalio.Direction.OUTPUT
            self.expLatch.direction = digitalio.Direction.OUTPUT
            self.expClock.direction = digitalio.Direction.OUTPUT
            self.expClear.direction = digitalio.Direction.OUTPUT
            self.expCS1.direction = digitalio.Direction.OUTPUT
            self.expCS2.direction = digitalio.Direction.OUTPUT
            self.expCS3.direction = digitalio.Direction.OUTPUT
            self.expAck.direction = digitalio.Direction.INPUT
            
            self.expData.value = False
            self.expLatch.value = False
            self.expClock.value = False
            self.expClear.value = False
            
            #Clear any registers
            self.expCS1.value = True
            self.expCS2.value = True
            self.expCS3.value = True
            time.sleep(.001)
            self.clearPulse()
            self.expCS1.value = False
            self.expCS2.value = False
            self.expCS3.value = False
        else:
            self.expData.deinit()
            self.expLatch.deinit()
            self.expClock.deinit()
            self.expClear.deinit()
            self.expCS1.deinit()
            self.expCS2.deinit()
            self.expCS3.deinit()
            self.expAck.deinit()
        
        self.expLampState = 0
            
    def clockPulse(self):
        self.expClock.value = True
        time.sleep(.001)
        self.expClock.value = False

    def latchPulse(self):
        self.expLatch.value = True
        time.sleep(.001)
        self.expLatch.value = False
        
    def clearPulse(self):
        self.expClear.value = True
        time.sleep(.001)
        self.expClear.value = False
        
    def lampExpSet(self, mask):
        self.expLampState |= mask
        
    def lampExpClear(self, mask):
        self.expLampState &= ~mask
        
    def writeLampExp(self):
        self.expCS1.value = True
        time.sleep(.001)
        
        
        for bitCounter in range(16):
            self.expData = (self.expLampState >> bitCounter) & 1
            time.sleep(.001)
            self.clockPulse()
        
        self.latchPulse()
    
    def processState(self, soundDatabus, voicePlaying):
        currentState = self.expLampState
        self.expLampState = 0
        
        if soundDatabus.engineTroubleState:
            self.expLampState |= EXP_ENGINE_LAMP_MASK
        if voicePlaying:
            self.expLampState |= EXP_COMM_LAMP_MASK         
        if soundDatabus.d0.value:
            self.expLampState |= EXP_STATE0_MASK
        if soundDatabus.d1.value:
            self.expLampState |= EXP_STATE1_MASK
        if soundDatabus.d2.value:
            self.expLampState |= EXP_STATE2_MASK
        if soundDatabus.d3.value:
            self.expLampState |= EXP_STATE3_MASK      
        
        if soundDatabus.voiceState == GAME_OVER:
            self.expLampState |= EXP_GAMEOVER_LAMP_MASK
        elif soundDatabus.voiceState == GAME_START:
            self.expLampState |= EXP_SCRAMBLE_MASK
        elif soundDatabus.voiceState == WAVE_COMPLETE:
            self.expLampState |= EXP_SUCCESS_LAMP_MASK
            self.expLampState |= currentState & (EXP_WAVE1_LAMP_MASK | EXP_WAVE2_LAMP_MASK | EXP_WAVE2_LAMP_MASK)
            
        if WAVE_1_CHARLIE <= soundDatabus.voiceState <= WAVE_1_CAUTION:
            self.expLampState |= EXP_WAVE1_LAMP_MASK
        elif WAVE_2_CHARLIE <= soundDatabus.voiceState <= WAVE_2_CAUTION:
            self.expLampState |= EXP_WAVE2_LAMP_MASK
        elif WAVE_3_CHARLIE <= soundDatabus.voiceState <= WAVE_1_CAUTION:
            self.expLampState |= EXP_WAVE3_LAMP_MASK
        
        if (soundDatabus.voiceState == WAVE_1_CHARLIE or
            soundDatabus.voiceState == WAVE_2_CHARLIE or
            soundDatabus.voiceState == WAVE_3_CHARLIE):
            self.expLampState |= EXP_CHARLIE_LAMP_MASK
        elif (soundDatabus.voiceState == WAVE_1_BRAVO or
            soundDatabus.voiceState == WAVE_2_BRAVO or
            soundDatabus.voiceState == WAVE_3_BRAVO):
            self.expLampState |= EXP_BRAVO_LAMP_MASK
        elif (soundDatabus.voiceState == WAVE_1_ALPHA or
            soundDatabus.voiceState == WAVE_2_ALPHA or
            soundDatabus.voiceState == WAVE_3_ALPHA):
            self.expLampState |= EXP_ALPHA_LAMP_MASK
        
        if currentState != self.expLampState:
            self.writeLampExp()
    
    