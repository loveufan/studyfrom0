#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

string subtractBigNumbers(string num1, string num2) {
    bool negative = false;
    if (num1.length() < num2.length() || (num1.length() == num2.length() && num1 < num2)) {
        swap(num1, num2);
        negative = true;
    }

    reverse(num1.begin(), num1.end());
    reverse(num2.begin(), num2.end());

    string result;
    int borrow = 0;

    for (size_t i = 0; i < num1.length(); ++i) {
        int sub = (num1[i] - '0') - borrow;
        if (i < num2.length()) sub -= (num2[i] - '0');

        borrow = (sub < 0) ? 1 : 0;
        if (sub < 0) sub += 10;

        result.push_back(sub % 10 + '0');
    }

    while (result.size() > 1 && result.back() == '0') {
        result.pop_back();
    }

    reverse(result.begin(), result.end());
    return negative ? "-" + result : result;
}