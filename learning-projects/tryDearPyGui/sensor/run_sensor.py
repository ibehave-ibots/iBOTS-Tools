import random
import struct
import sys
import time
from math import sin

SAMPLING_RATE_HZ = 100_000

while True:
    # time.sleep(1 / SAMPLING_RATE_HZ)
    time.sleep(0.0000000000000000000000000000000001)
    t = time.perf_counter()
    y = sin(8 * t + .2 * random.random())
    packet = struct.pack('dd', t, y)
    try:
        sys.stdout.buffer.write(packet)
        sys.stdout.buffer.flush()
    except BrokenPipeError:
        break
    