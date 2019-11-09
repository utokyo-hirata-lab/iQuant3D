#include "peak_detection.h"

int c_peak_detect(int *num1, int *num2, int size_a, int size_b){
    int res = 0;
    for(int i=0; i < size_a; i++){
        for(int j=0; j < size_b; j++){
            res = res + num1[i]+num2[j];
        }
    }
    return res;
}
