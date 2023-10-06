#include <iostream>
#include <math.h>
using namespace std;

int main(){
    double tmp = log(2024.0/2023.0);
    cout << 0 << ": " << tmp << endl;
    for(int i=1; i<21; i++){
        tmp = 1.0/i - 2023*tmp;
        if(i%2==0)
            cout << i << ": " << tmp << endl;
        else
            cout << "                           " << i << ": " << tmp << endl;
    }

    return 0;
}
//chyba ok 