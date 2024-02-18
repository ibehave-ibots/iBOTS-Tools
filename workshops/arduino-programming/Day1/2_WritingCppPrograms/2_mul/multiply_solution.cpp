//  Directions: Create the following functions:
//     - int multiply3(int x, int y, int z): multiplies the numbers together.
//     - int main(): calls multiply3() on the numbers 4, 5, and 6, and prints the result.
//    (Bonus Points): Let's make the multiply3() function sharable, seperate from the main() function:
//           1. Put the multiply3() function into a file called `mul.h`, 
//           2. Put #include "mul.h" in the header to import the code.

// Library Reference:
  // #include <cstdio>
    // printf("%d\n", 4)        (prints the integer 4 and then starts a new line)
    // printf("%d,%d\n", 5, 6)  (prints "5,6" and then a new line )
    // the printf() table describing the formats can be found at https://cplusplus.com/reference/cstdio/printf/


#include <cstdio>

int mul(int x, int y) {
    return x * y;
}

int main(int argc, char *argv[]) {
    printf("%d\n", mul(3, 4));
}
