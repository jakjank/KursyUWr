#include <iostream>
#include <math.h>
using namespace std;

int main(){

    double y0 = 1.0;
    double y1 = -1.0 / 9.0;
    double y2;
    cout<<"0: "<<y0<<endl;
    cout<<"1: "<<y1<<endl;
    for(int i=2;i<51;i++)
    {   
        y2 = 80.0/9.0*y1 + y0;
        cout<<i<<": 80/9*"<<y1<<"+"<<y0<<" = "<<y2<<endl;
        y0 = y1;
        y1 = y2;
    }
    return 0;
}
//nie sa to wyniki wiarygodne, bo powinien to być ciag malejacy