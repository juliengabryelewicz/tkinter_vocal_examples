import json
import pyaudio
import threading
import tkinter as tk
from vosk import Model, KaldiRecognizer

class ColorChange(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Change color with voice")
        self.geometry("300x400")

    def change_background_color(self, text):
        switcher = {
            "rouge": "#FF0000",
            "vert": "#00FF00",
            "bleu": "#0000FF"
        }
        color_chosen = switcher.get(text, "grey")
        if color_chosen != "grey":
            self['bg']=color_chosen

def listen_microphone():
    while True:
        data = stream.read(8000, exception_on_overflow = False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            color_change.change_background_color(result["text"])
    #color_change.after(8000, listen_microphone)

if __name__ == "__main__":
    color_change = ColorChange()

    ##PYAUDIO
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    ##VOSK
    model = Model("model/fr_FR")
    rec = KaldiRecognizer(model, 16000)

    thread = threading.Thread(target=listen_microphone)
    thread.daemon = True 
    thread.start()

    color_change.mainloop()