// 定义一个函数来检测一个数是否为素数
bool isPrime(int num) {
    // 素数定义要求大于 1
    if (num <= 1) return false;
    // 2 是最小的素数
    if (num == 2) return true;
    // 偶数（除 2 外）都不是素数
    if (num % 2 == 0) return false;
    // 从 3 开始，只检查奇数，直到平方根
    for (int i = 3; i * i <= num; i += 2) {
        if (num % i == 0) return false;
    }
    // 如果没有找到因子，则是素数
    return true;
}
