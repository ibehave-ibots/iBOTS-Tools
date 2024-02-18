// Directions:  Print the text, "Hello World!" to the Terminal

// Reference:

  // Writing C++ Code in the Editor:
    // #include <iostream>            (Gives you "std::cout" to print to the terminal.)
    // int main(){}                   (The main function that will be automatically run when the program starts)
    // std::cout << "Hello!\n"        (Print the test "Hello!" to the terminal)

  // Running the Code In the Terminal:
    // cd 1_hello                     (Changes the current directory to the 1_hello directory)
    // cd ..                          (Changes the current directory to the parent directory.)
    // g++ hello.cpp -o hello         (Runs the g++ compiler to make an executable from the source code)
    // ./hello                        (Runs the executable.)
    // g++ hello.cpp -o hello && hello (Compile and run at the same time.)
    

    
#include <iostream>

int main(){
    std::cout << "Hello, World!\n";
}