// Directions:  Create the following functions:
  // void print(char[] message): prints a message to the terminal.
  // void delay(int milliseconds): pauses the program for the specifed amount of time.
  // int main(): Uses the created functions to do the following in an endless loop:
    //  print "Sleeping...", wait 1.5 seconds, 
    //  then print, "Awake!", wait 0.5 seconds,
    //  then repeat.

// Library Reference:
    // <cstdio>:  Contains code for inputs from and outputs to the terminal.
        // printf("Hi\n"): prints "Hi" then a new line
        // fflush(stdout): forces what is being printed to immediately show up, even if there is no new line character.
    // <chrono>:  Contains code for describing time.
        // std::chrono::seconds(int secs): make some seconds value of type "chrono::duration".
        // std::chrono::milliseconds(int milli): make some milliseconds value of type "chrono::duration".
    // <thread>: Contains code for interacting with the current thread, regardless of operating system.
        // std::this_thread::sleep_for(chrono time)

// Syntax Reference:
    // using namespace std;   (Makes it so you don't always have to write "std::")
    // while (true) {};   (An endless loop)


#include <cstdio>
#include <thread>
#include <chrono>

using namespace std;
int main(){
    while (true) {
        printf("Sleeping...");
        fflush(stdout);

        chrono::duration millis = chrono::milliseconds(1500);
        this_thread::sleep_for(millis);
        printf("Awake!\n");
    }
}