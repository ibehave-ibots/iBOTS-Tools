# Learning Project: Asynchronous Coding and Dear PyGui

This is a small project to explore some of the built-in python tools around parallel processing, using an example of displaying a real-time signal that is being collected by some sensor.  

Some things I wanted to learn:
  - What's it like to use DearPyGui, and does it seem like a useful tool for data collection applications?  I've already come to like Streamlit
  for web apps, and I'm happy with FastAPI, but somehow Tkinter and PyQt have only been marginal
  successes in my book, and Vispy and Kivy never matured enough for me to be totally happy with real-time data applications.  DearPyGui has potential.

  - Can I find some simple, reusable patterns for organizing and composing together multiple data streams? 


After playing around a bit with `threading`, `multiprocessing`, and `asynicio`, I settled on using a combination of multiprocessing and asyncio: 
  - Multiprocessing's `Manager` to separate each script into its own environment and define a clear interface between the two. (which should be even cleaner and higher-perfoamnce from Python 3.12 onward, now that seperate GILs are being put in place for each process).

  - Separate AsynicIO event loops for each process, with async functions to help increase the performance of IO-bound signals (here, that's mainly graphic rendering and console writing and reading)


Some Learnings:
  - New Functions/classes:
    - `multiprocessing.Manager`
    - `asyncio.ensure_future()`
    - `sys.stdout.buffer.write()` and `flush()`
        - Much higher-performance version of `print()`, useful for simulating the high-speed sensor (I think I got about 10kHz)
  - DearPyGui is pretty great!  I particularly liked how simple it was to implement an asynicio-based event loop.  Also, keeping the Gui responsive was really straightforward, as was debugging problems.  Very nice!
  - There were some interesting bugs while handling the data stream; in the future, it might be good to automate performance testings to verify these tradeoffs (what "Evolutionary Architecture" calls "fitness functions"), as they were really subtle and time-consuming to track down.


Overall, really neat!  

