### Structure of an Arduino Program

In an Arduino program, you don't write your code into a function called 
`main()`, even though you're still writing C++.  Instead, you write your
code into two important functions: `void setup()` and `void loop()`:

  - `setup()` is called one time, when the device starts.
  - `loop()` is called afterward, repeatedly, forever.

If both functions need to use the same variable, the variable is defined
outside the function.  

This is an example of a "Framework": a system that calls your code.  This is different from a library, which has code that your code calls.  Arduino has both; library functions that let you control the device (which we'll explore tomorrow), and the framework that it expects code to be written in.

### Exercise

Recreate the Arduino framework and library in order to make an imaginary LED light attached to the imaginary Arduino digital IO pin number 3 blink on and off, by making:

   - `arduino.h`: Contains the functions:
      - `void delay(int millisecs)`
      - `void print(char[] message)`
      - `void digitalWrite(int pin, bool value)`
          - if `pin` is 5 and `value` is true, then prints "Pin 5 is HIGH".
          - if `pin` is 5 and `value` is false, then prints "Pin 5 is LOW".
   - `main.cpp`: Just calls `setup()` once, then `loop()` endlessly, getting the functions in `my_project.h`
   - `my_project.h`: Contains the functions `setup()` and `loop()`, to:
      1. Print "Device is on." once.
      2. Print "Pin 3 is HIGH", then "Pin 3 is LOW", at 0.5-second intervals.



