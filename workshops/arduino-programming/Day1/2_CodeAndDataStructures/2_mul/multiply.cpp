//  Directions: Create the following functions:
//     - int multiply3(int x, int y, int z): multiplies the numbers together.
//     - int main(): calls multiply3() on the numbers 4, 5, and 6, and prints the result.
//    (Bonus Points): Let's make the multiply3() function sharable, seperate from the main() function:
//           1. Put the multipley3() function into a file called `mul.h`, 
//           2. Put #include "mul.h" in the header to import the code.

#include <cstdlib>
#include<iostream>
#include "mul.h"

using namespace std;


int main(int argc, char *argv[]) {
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    cout << mul(x, y);
}
