#include <iostream>
#include <math.h>

using namespace std;

// a = sqrt(x^14 + 1), b = 1
// a-b / (a-b)(a+b) = 1 / (a+b)

double f(double x){
    return 4046 / (sqrt(pow(x,14) + 1) + 1);
}

int main(){
    cout << f(0.001) << endl;
    return 0;
}