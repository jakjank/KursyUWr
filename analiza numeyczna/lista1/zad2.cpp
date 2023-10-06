#include <iostream>
#include <math.h>
using namespace std;

double f(double x){
    return 4046 * (sqrt(pow(x,14) + 1) + 1) / pow(x,14);
}

int main(){
    cout << f(0.001) << endl;
    return 0;
}
//zle, powinno wyjsc 20203