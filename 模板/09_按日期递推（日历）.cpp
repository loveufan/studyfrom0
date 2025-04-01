#include <iostream>
#include <vector>
using namespace std;

// 判断闰年
bool isLeapYear(int year) {
    return (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
}

// 获取月份天数
int getMonthDays(int year, int month) {
    vector<int> days = {31,28,31,30,31,30,31,31,30,31,30,31};
    if(month == 2 && isLeapYear(year)) return 29;
    return days[month-1];
}

// 计算下一天日期
void nextDay(int &year, int &month, int &day) {
    day++;
    if(day > getMonthDays(year, month)) {
        day = 1;
        month++;
        if(month > 12) {
            month = 1;
            year++;
        }
    }
}

// 计算N天后的日期
void addDays(int &year, int &month, int &day, int n) {
    while(n--) {
        nextDay(year, month, day);
    }
}