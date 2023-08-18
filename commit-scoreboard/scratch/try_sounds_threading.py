import numpy as np
import sounddevice as sd
import threading

import numpy as np
import sounddevice as sd

# def generate_tone(frequency, duration, samplerate=44100):
#     t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
#     envelope = np.exp(-t * 3)  # An exponential decay to make it sound more like a chime
#     tone = np.sin(2 * np.pi * frequency * t) * envelope
#     return tone

# G Major scale frequencies for the 4th and 5th octaves
frequencies = [
    392.00,  # G4
    440.00,  # A4
    493.88,  # B4
    523.25,  # C5
    587.33,  # D5
    659.25,  # E5
    783.99,  # G5
    880.00,  # A5
    987.77   # B5
]

g_major_chord_frequencies = [
    196.00,  # G3
    246.94,  # B3
    293.66,  # D4
    392.00,  # G4
    493.88,  # B4
    587.33,  # D5
    783.99,  # G5
    987.77,  # B5
    1174.66  # D6
]

# Play each note in the scale for 0.5 seconds
for freq in g_major_chord_frequencies:
    tone = generate_chime_tone(freq, 0.5) * .2
    sd.play(tone)
    sd.wait()


# Function to generate the tone
def generate_tone(frequency, duration, samplerate=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    envelope = np.exp(-t * 3)  # Exponential decay to simulate a chime
    tone = np.sin(2 * np.pi * frequency * t) * envelope
    return tone

# Function to play the tone
def play_tone(frequency, duration):
    tone = generate_tone(frequency, duration)
    sd.play(tone)

# When an event arrives, call this function
def on_event(frequency=440.0):
    threading.Thread(target=play_tone, args=(frequency, 1.5)).start()

# Simulate events
on_event(440.0)
on_event(550.0)