#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <random>

using namespace std;

int main(){
    int iters;
    cout << "Enter number of iterations: ";
    cin >> iters;
    cout << endl;
    double x;
    double y;
    int num_inside = 0;
    int num_outside = 0;
    default_random_engine generator;
    generator.seed(time(0));
    uniform_real_distribution<double> distribution(0.0,1.0);

    for(int i = 0; i < iters; i++){
        x = distribution(generator);
        y = distribution(generator);
        if(x*x + y*y >= 1){
            num_outside++;
        } else {
            num_inside++;
        }
    }
    // cout.precision(15);
    double pi = 4.0 * num_inside / (num_inside + num_outside);
    cout << "pi = " << scientific << pi << endl;
    return 0;
}
