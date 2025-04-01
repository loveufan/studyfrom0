#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

string multiplyBigNumbers(string num1, string num2) {
    if (num1 == "0" || num2 == "0") return "0";

    reverse(num1.begin(), num1.end());
    reverse(num2.begin(), num2.end());
    
    vector<int> product(num1.size() + num2.size(), 0);

    for (size_t i = 0; i < num1.size(); ++i) {
        for (size_t j = 0; j < num2.size(); ++j) {
            product[i + j] += (num1[i] - '0') * (num2[j] - '0');
            product[i + j + 1] += product[i + j] / 10;
            product[i + j] %= 10;
        }
    }

    while (product.size() > 1 && product.back() == 0) {
        product.pop_back();
    }

    string result;
    for (auto it = product.rbegin(); it != product.rend(); ++it) {
        result.push_back(*it + '0');
    }

    return result;
}