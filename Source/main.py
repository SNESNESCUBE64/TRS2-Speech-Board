import board
import digitalio
import time
import audiomp3
import audiopwmio

import TRS2_VoiceConfig
import TRS2_VoiceDriver
import TRS2_TestMode
import TRS2_Exp

#Wait for the EZ20 amp to start up
time.sleep(1)

#Initialization
soundDatabus = TRS2_VoiceConfig.SoundDatabus()
soundDatabus.init()
voiceSettings = TRS2_VoiceConfig.VoiceSettings()
voiceSettings.init()
voiceDriver = TRS2_VoiceDriver.VoiceDriver()
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False
testButton = digitalio.DigitalInOut(board.GP14)
testButton.direction = digitalio.Direction.INPUT

time.sleep(.1)
voiceSettings.readDipSwitches()
voiceDriver.voiceSet = voiceSettings.speechSet
voiceDriver.startupSet = voiceSettings.startupSound

exp = TRS2_Exp.ExpDriver()
exp.init(voiceSettings.expEnable)

soundDatabus.updateVoiceState()
lastVoiceState = soundDatabus.voiceState

#In case for some reason the user doesn't want the audio boad to play
while voiceSettings.muted:
    if not testButton.value:
        TRS2_TestMode.selfTest(soundDatabus, exp, voiceSettings, voiceDriver, testButton)
        while not testButton.value:
            pass

#Play the startup sound if 
if voiceSettings.startupSound > 0:
    led.value = True
    soundDatabus.ack.value = False
    voiceDriver.playStartup()
    while voiceDriver.voice.playing:
        pass
    led.value = False
    soundDatabus.ack.value = True
        
        
engineTroubleCounter = 0
engineTroubleMax = voiceSettings.engineTroubleDelay

#main loop
while True:
    soundDatabus.updateVoiceState()
    
    if not testButton.value:
        led.value = True
        soundDatabus.ack.value = False
        TRS2_TestMode.selfTest(soundDatabus, exp, voiceSettings, voiceDriver, testButton)
        led.value = False
        soundDatabus.ack.value = True
        while not testButton.value: #this should take priority
            pass
        time.sleep(.2)
        
    #check for a change in the state
    if lastVoiceState != soundDatabus.voiceState:
        time.sleep(.2)
        compState = soundDatabus.voiceState
        soundDatabus.updateVoiceState()
        #double check that it wasn't a blip
        if compState == soundDatabus.voiceState:          
            while voiceDriver.voice.playing:
                pass
            led.value = True
            soundDatabus.ack.value = False
            voiceDriver.playVoice(soundDatabus.voiceState)
            lastVoiceState = soundDatabus.voiceState
    
    #Check if there is an engine trouble status       
    if engineTroubleMax > 0:
        if soundDatabus.engineTroubleState and not voiceDriver.voice.playing and engineTroubleCounter == 0:
            time.sleep(.2)
            soundDatabus.updateVoiceState()
            #double check that it wasn't a blip
            if soundDatabus.engineTroubleState:          
                led.value = True
                soundDatabus.ack.value = False
                voiceDriver.playVoice(16)
                engineTroubleCounter += 1
        
        #If the engine trouble voice played, increment the delay counter
        if soundDatabus.engineTroubleState and not voiceDriver.voice.playing:
            engineTroubleCounter += 1
            time.sleep(.1)
        
        #If we reach the threshold, reset the counter so the line can be played
        if engineTroubleCounter > engineTroubleMax or not soundDatabus.engineTroubleState:
            engineTroubleCounter = 0     
    
    #Turn the LED off whenever the module is done speaking
    if not voiceDriver.voice.playing:
        led.value = False
        soundDatabus.ack.value = True
    
    #For expansion lamp driver
    if voiceSettings.expEnable:
        exp.processState(soundDatabus, voiceDriver.voice.playing)
        
print("Should never reach this point")
