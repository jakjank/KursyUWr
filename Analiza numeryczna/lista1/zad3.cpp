#include <iostream>
#include <math.h>
using namespace std;

double f_double(double x){
    return 14 * (1-cos(17*x)) / x / x;
}

float f_single(float x){
    return 14 * (1-(float)cos(17*x)) / x / x;
}

int main(){
    cout << "Double" << endl;
    for(int i=11; i<=20; i++){
        cout<<i <<": "<< f_double(pow(10,-i)) << endl;
    }
    cout << endl << "Single" << endl;
    for(int i=11; i<=20; i++){
        cout<<i <<": "<< f_double(pow(10,-i)) << endl;
    }
    return 0;
}
//czy otrzymane wyniki sa poprawne?