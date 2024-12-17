#include <stdio.h>

/*
 * Throwaway program to explore candidate solutions
 */
int main(int argc, char** argv) {
    int expected[] = {2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0};
    printf("%d\n", sizeof(__int128));
    
    for (long long a_input = 27200000000l;;a_input++) {
        if(a_input % 1000000000 == 0) {
            printf("\na=%lld", a_input);
        }
        
        long long a = a_input;
        int i_out = 0;
        while (a) {
            int out = (a ^ (a >> ((a & 0b111) ^ 0b11))) & 0b111;
            a = a >> 3;
            // printf("%d:%d,", out, expected[i_out]);
            if (out != expected[i_out]) {
                break;
            }
            i_out++;
        }
        // printf("\n");
        if (i_out >= 6) {
            printf("\n\nanswer=%lld\n", a_input);
            return 0;
        }
    }
}
