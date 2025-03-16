import board
import digitalio
import time
import audiomp3
import audiopwmio

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
ENGINE_TROUBLE = 16

SPEECH_SET = ["Trouble.mp3",
              "Charlie.mp3",
              "Bravo.mp3",
              "Alpha.mp3",
              "UseCaution.mp3",
              "Complete.mp3",
              "EngineTrouble.mp3"]

STARTUP_SET = ["SayItLowStartup.mp3",
               "SayItHighStartup.mp3",
               "BonziStartup.mp3"]

BASE_PATH = "SoundSamples/"
    
class VoiceDriver:   
    voice = audiopwmio.PWMAudioOut(board.GP16)
    voiceSet = 0
    startupSet = 0
    currentFile  = open((BASE_PATH + "Set" + str(voiceSet) + "/" + SPEECH_SET[0]), "rb")
    decoder = audiomp3.MP3Decoder(currentFile)
        
    def playVoice(self, voiceID):
        speechSampleID = processSpeechID(voiceID, self.voiceSet)
        if speechSampleID != -1:
            self.currentFile.close()
            self.currentFile = open((BASE_PATH + "Set" + str(self.voiceSet) + "/" + SPEECH_SET[speechSampleID]), "rb")
            self.decoder.file = self.currentFile
            self.voice.play(self.decoder)
            
    def playStartup(self):
        if self.startupSet != 0:
            self.currentFile.close()
            self.currentFile = open((BASE_PATH + "Startup/" + STARTUP_SET[self.startupSet-1]), "rb")
            self.decoder.file = self.currentFile
            self.voice.play(self.decoder) 

def processSpeechID(status, speechSet):
    sampleID = -1
    
    if(status == GAME_START):
        sampleID = 0
    elif(status == WAVE_1_CHARLIE or status == WAVE_2_CHARLIE or status == WAVE_3_CHARLIE):
        sampleID = 1
    elif(status == WAVE_1_BRAVO or status == WAVE_2_BRAVO or status == WAVE_3_BRAVO):
        sampleID = 2
    elif(status == WAVE_1_ALPHA or status == WAVE_2_ALPHA or status == WAVE_3_ALPHA):
        sampleID = 3
    elif(status == WAVE_1_CAUTION or status == WAVE_2_CAUTION  or status == WAVE_3_CAUTION):
        sampleID = 4
    elif(status == WAVE_COMPLETE):
        sampleID = 5
    elif(status == ENGINE_TROUBLE):
        sampleID = 6
    
    return sampleID

def setTalking(talking):
    pass
        