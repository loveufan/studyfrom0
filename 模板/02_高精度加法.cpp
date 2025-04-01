// 高精度加法函数
string addBigNumbers(const string& num1, const string& num2) {
    string result;
    int carry = 0;
    int i = num1.size() - 1;
    int j = num2.size() - 1;

    // 从两个数的最低位开始逐位相加
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += num1[i--] - '0';
        if (j >= 0) sum += num2[j--] - '0';
        result.push_back(sum % 10 + '0');
        carry = sum / 10;
    }

    // 反转结果字符串以得到正确的顺序
    reverse(result.begin(), result.end());
    return result;
}
