import time
import TRS2_VoiceConfig
import TRS2_VoiceDriver

MODULE_MAJOR_REVISION = 1
MODULE_MINOR_REVISION = 0

def selfTest(soundDatabus, exp, voiceSettings, voiceDriver, testButton):
    while not testButton.value:
            pass
    voiceDriver.voice.stop()   
    print("TRS2 Voice Module Self Test")
    print("Software Version " + str(MODULE_MAJOR_REVISION) + "." + str(MODULE_MINOR_REVISION))
    print("SNESNESCUBE64")
    print("=======================================")
    print("Current Sound Bus State: " + str(soundDatabus.voiceState))
    print("Engine Trouble State: " + str(soundDatabus.engineTroubleState))
    
    #read the dip switch options back
    dipSwitchValue = voiceSettings.dipsw0.value * 1
    dipSwitchValue += voiceSettings.dipsw1.value * 2
    dipSwitchValue += voiceSettings.dipsw2.value * 4
    dipSwitchValue += voiceSettings.dipsw3.value * 8
    dipSwitchValue += voiceSettings.dipsw4.value * 16
    dipSwitchValue += voiceSettings.dipsw5.value * 32
    dipSwitchValue += voiceSettings.dipsw6.value * 64
    dipSwitchValue += voiceSettings.dipsw7.value * 128   
    print("Dip Switches: " + str(bin(dipSwitchValue)))
    print("Muted: " + str(voiceSettings.muted))
    print("Speech Set: " + str(voiceSettings.speechSet))
    print("Startup Sound Enable: " + str(voiceSettings.startupSound))
    print("Engine Trouble Sound Delay Setting: " + str(voiceSettings.engineTroubleDelay))
    print("Expansion Enable: " + str(voiceSettings.expEnable))
    
    #play back all audio
    print("Playing all samples..." ) 
    testVoiceSequence = [1,4,5,6,15,3,16]
    endEarly = False
    for testVoiceID in testVoiceSequence:
        voiceDriver.playVoice(testVoiceID)
        #End the test early if the button is pressed
        while voiceDriver.voice.playing and not endEarly:
            if not testButton.value:
                endEarly = True
                voiceDriver.voice.stop() 
        time.sleep(.2)
        if endEarly:
            break
    
    while not testButton.value:
        pass
    time.sleep(.1)
    
    #Expansion Lamp Test
    if exp.expEnable:
        print("Lamp Test -  Press test button to exit")
        sleepCounter = 0
        exp.expLampState = 0x8000
        exp.writeLampExp()
        while testButton.value:
            if sleepCounter == 3:
                exp.writeLampExp()
                sleepCounter = 0
                exp.expLampState = exp.expLampState >> 1
                if exp.expLampState == 0:
                    exp.expLampState = 0x8000
                print("Current Lamp Value: " + str(hex(exp.expLampState)))
            else:
                sleepCounter += 1
            time.sleep(.1)
    
    print("Self Test Complete")
    print()