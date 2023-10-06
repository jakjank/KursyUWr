#include <iostream>
#include <math.h>
using namespace std;

int main(){
    double my_pi = 0;
    for(int i=0; i<2000001; i++){
        my_pi += (4.0 * pow(-1,i)) / (2*i + 1);
        if(i%1000 == 0)
            cout<<i<<": "<<my_pi<<" - "<<abs(my_pi - M_PI)<<endl;
    }
    
    return 0;
}
//chyba git, ale mamy dokladnosc rzedu 10^-6 juz po milionie wyrazow a nie po dwoch 