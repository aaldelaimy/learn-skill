# Exercise format

Template file: `practice/exN.<ext>`. The user writes every function. The file gives the spec as comments and a `main` (or test block) that already calls the functions and shows the expected output.

Rules:
- **No function signatures or stubs.** For each function, give its name, inputs, what it returns, and any rule or hint, as comments. The user writes the header themselves.
- Parts go from a warm-up to the real task. Add one "FIND THE BUG: don't just fix it, write a comment explaining WHY" part when the lesson has a classic mistake.
- Every call in `main` has its expected result in a trailing comment, or the full expected output in a block comment at the end.
- Test edge cases in `main` too: empty input, negatives, the last index, growing past capacity.
- Never put the solution in the file. Hints go in the spec comments ("hint: what should max start as? not 0").

Example (C):

```c
#include <stdio.h>

// Write everything below yourself, above main.
//
// 1. divide
//    Inputs:  two ints a and b, plus somewhere to put the quotient and the remainder
//    Returns: nothing; it "returns" two answers through pointers
//
// 2. FIND THE BUG: set_to_zero below should set the caller's variable to 0.
//    Fix it, and write a comment explaining WHY the original doesn't work.
void set_to_zero(int *p) {
    p = 0;
}

int main(void) {
    int q, r;
    divide(17, 5, &q, &r);
    printf("17 / 5 = %d remainder %d\n", q, r);   // 17 / 5 = 3 remainder 2

    int y = 42;
    set_to_zero(&y);
    printf("y = %d\n", y);                        // y = 0
    return 0;
}
```

For Python, the same idea: comments describe each function, and an `if __name__ == "__main__":` block (or a pytest file the user grows) checks the results.
