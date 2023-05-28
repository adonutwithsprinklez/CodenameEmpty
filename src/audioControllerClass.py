

import simpleaudio as sa

class AudioController(object):
    def __init__(self, raiseExceptions=True):
        self.audioLayers = {}
        self.bufferedAudio = {}
        self.mute = False
        self.raiseExceptions = raiseExceptions
    
    def bufferAudio(self, name, path):
        self.bufferedAudio[name] = sa.WaveObject.from_wave_file(path)
    
    def addLayer(self, name):
        self.audioLayers[name] = AudioLayer(name)
    
    def playAudio(self, layer, audioBuffer, queue=True, repeat=False):
        if not self.mute:
            self.audioLayers[layer].play(audioBuffer, queue, repeat)
    
    def playBufferedAudio(self, layer, name, queue=True, repeat=False):
        
        # Disabled due to SimpleAudio not being thread safe
        # Will re-enable when I find a better audio library
        return None

        # Check if audio is buffered
        if not name in self.bufferedAudio.keys():
            if self.raiseExceptions:
                raise Exception(f"Audio {name} not buffered")
            else:
                print("ERR - Audio {name} is not buffered.")
        elif not self.mute:
            self.playAudio(layer, self.bufferedAudio[name], queue, repeat)
    
    def setMuteAll(self, mute):
        self.mute = mute
    
    def setMuteLayer(self, layer, mute):
        self.audioLayers[layer].setMute(mute)
    
    def stopAll(self):
        for layer in self.audioLayers.keys():
            self.audioLayers[layer].stop(True)
    
    def updateAll(self, forceStop=False):
        for layer in self.audioLayers.keys():
            self.audioLayers[layer].update(forceStop or self.mute, forceStop or self.mute)

class AudioLayer(object):
    def __init__(self, name):
        self.name = name
        self.currentAudio = None
        self.currentAudioObject = None
        self.audioQueue = []
        self.repeat = False
        self.mute = False
    
    def setMute(self, mute):
        self.mute = mute
    
    def update(self, stop=False, clearQueue=False):
        if stop or self.mute:
            self.stop(clearQueue)
        if self.currentAudio == None or not self.currentAudio.is_playing():
            self.currentAudio = self.getNextAudio()
    
    def stop(self, clearQueue=True):
        if self.currentAudio != None:
            self.currentAudio.stop()
            self.currentAudio = None
            self.currentAudioObject = None
        if clearQueue:
            self.audioQueue = []
    
    def getNextAudio(self):
        if self.repeat and self.currentAudioObject != None:
            return self.currentAudioObject.play()
        if len(self.audioQueue) > 0:
            return self.audioQueue.pop(0).play()
        return None
    
    def play(self, audioBuffer, queue=True, repeat=False):
        if not self.mute:
            if not repeat or (repeat and self.currentAudioObject != audioBuffer):
                if queue:
                    self.audioQueue.append(audioBuffer)
                else:
                    self.stop(True)
                    self.audioQueue = [audioBuffer]
                    self.currentAudioObject = audioBuffer
                    self.repeat = repeat
        self.update(False, not queue)


'''


if __name__ == "__main__":
    RES = "res/official/audio/"

    FILES = {
        "click1":"click4.wav",
        "click2":"click5.wav",
        "other":"death.wav",
        "end":"round_end.wav"
    }

    import time

    loadedData = {}
    for key in FILES.keys():
        loadedData[key] = sa.WaveObject.from_wave_file(RES + FILES[key])
    audioController = AudioController()
    audioController.addLayer("click")
    audioController.addLayer("LongSound")
    for i in range(10):
        audioController.play("click", loadedData["click1"])
        audioController.play("click", loadedData["click2"])
    for i in range(20):
        audioController.updateAll()
        print(i)
        time.sleep(0.01)
    audioController.play("LongSound", loadedData["other"], False, True)
    for i in range(5):
        audioController.play("click", loadedData["click1"])
        audioController.play("click", loadedData["click2"])
    for i in range(100):
        audioController.updateAll()
        print(i)
        time.sleep(0.01)
    audioController.play("LongSound", loadedData["end"], False, False)
    for i in range(200):
        audioController.updateAll()
        print(i)
        time.sleep(0.01)
'''