from collections import defaultdict
import random

import numpy as np
import sounddevice as sd

from scoreboard.core.app import SoundSpeaker


class SounddeviceSpeaker(SoundSpeaker):

    def __init__(self) -> None:
        self.tones = [generate_chime_tone(freq, .7) for freq in am7_chord_frequencies]
        self.team_tones = defaultdict(self._consume_random_tone)
        
    def _consume_random_tone(self) -> np.ndarray:
        random.shuffle(self.tones)
        return self.tones.pop()
    
    def play_team_sound(self, team, blocking: bool = False) -> None:
        tone = self.team_tones[team]
        sd.play(tone, blocking=False)
        if blocking:
            sd.wait()


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
        0.3 * np.sin(2 * np.pi * 3 * frequency * t)
    ]

    # Combine the tones and apply the envelope
    combined_signal = np.sum(harmonics, axis=0) * envelope
    return combined_signal



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

am7_chord_frequencies = [
    # 220.00,   # A3
    261.63,   # C4
    329.63,   # E4
    392.00,   # G4
    440.00,   # A4
    523.25,   # C5
    659.25,   # E5
    783.99,   # G5
    880.00,   # A5
    1046.50,  # C6
    # 1318.51,  # E6
    # 1567.98   # G6
]