# %% ChatGPTs attempt at a windchime
import time
import numpy as np
import sounddevice as sd
import threading


def generate_chime_tone(frequency, duration, samplerate=44100):
    # Generate time vector
    t = np.linspace(0, duration, int(samplerate * duration * 1.5), endpoint=False)
    
    # Create a linear attack envelope
    attack_duration = 0.1
    attack_samples = int(samplerate * attack_duration)
    attack_envelope = np.linspace(0, 1, attack_samples)

    # Create a decaying amplitude envelope
    envelope = np.exp(-t * 12)
    envelope[:len(attack_envelope)] *= attack_envelope

    # Generate the primary tone and some harmonics
    harmonics = [
        np.sin(2 * np.pi * frequency * t),
        0.5 * np.sin(2 * np.pi * 2 * frequency * t),
        # 0.3 * np.sin(2 * np.pi * 3 * frequency * t)
    ]

    # Combine the tones and apply the envelope
    combined_signal = np.sum(harmonics, axis=0) * envelope

    return combined_signal

# %%

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

tones = [generate_chime_tone(freq, .7) for freq in g_major_chord_frequencies]

# Play each note in the scale for 0.5 seconds
# for tone in tones[:]:
#     sd.play(tone)
#     sd.wait()



# %% Play Multiple, Overlapping tones, using threads

import numpy as np
import sounddevice as sd

# Function to play the tone
def play_tone(tone):
    sd.play(tone)

# When an event arrives, call this function
def on_event(tone):
    threading.Thread(target=play_tone, args=(tone,)).start()

# Simulate events
for tone in tones:
    on_event(tone)
    time.sleep(0.2)
    # sd.play(tone)
    # sd.wait()
# on_event(440.0)
# on_event(550.0)

