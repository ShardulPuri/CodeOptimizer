// sample.c - Simple C code for testing the TAC generator
// Avoiding preprocessor directives for easier parsing

int main() {
    int a;
    int b;
    int c;
    int d = 10;
    int e = 20;
    
    a = 5;
    b = 7;
    c = a + b;
    
    int f = c * d;
    int g = f / e;
    
    int h = (a + b) * (c - d);
    
    return 0;
}