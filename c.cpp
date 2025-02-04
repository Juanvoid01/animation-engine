



int max(int a, int b) {

    int max_number;

    if (a > b) {
        max_number = a;
    } else {
        max_number = b;
    }

    return max_number;
}



int max(int a, int b) {

    int max_number =  a * (a > b) + b * (a <= b);

    return max_number;
}