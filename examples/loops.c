#include <stdio.h>
#include <stdlib.h>

int main() {
    int i = 0;
    while ((i < 5)) {
        printf("%d\n", i);
        i = (i + 1);
    }
    int sum = 0;
    int j = 1;
    while ((j <= 10)) {
        sum = (sum + j);
        j = (j + 1);
    }
    printf("%d\n", sum);
    return 0;
}