//
#include <cstdlib>
#include<iostream>
using namespace std;

int mul(int x, int y) {
    return x * y;
}

int main(int argc, char *argv[]) {
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    cout << mul(x, y);
}