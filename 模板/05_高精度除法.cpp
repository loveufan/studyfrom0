#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

pair<string, string> divideBigNumbers(string dividend, string divisor) {
    if (divisor == "0") throw invalid_argument("Divisor cannot be zero");
    
    string result;
    string current;
    int index = 0;
    
    while (index < dividend.size()) {
        current += dividend[index++];
        int count = 0;
        
        while (current.size() > 1 && current[0] == '0') {
            current.erase(0, 1);
        }
        
        while (current.size() > divisor.size() || (current.size() == divisor.size() && current >= divisor)) {
            string temp = current;
            string subResult;
            
            for (int i = 0; i < temp.size() - divisor.size() + 1; ++i) {
                int num = 0;
                while (temp.size() >= divisor.size() + i && 
                      (temp.substr(0, divisor.size() + i) > divisor || 
                       temp.substr(0, divisor.size() + i) == divisor)) {
                    string sub = temp.substr(0, divisor.size() + i);
                    sub = to_string(stoi(sub) - stoi(divisor));
                    temp.replace(0, divisor.size() + i, sub);
                    num++;
                }
                subResult += to_string(num);
            }
            
            current = temp;
            count++;
        }
        
        result += to_string(count);
    }
    
    result.erase(0, min(result.find_first_not_of('0'), result.size()-1));
    current.erase(0, min(current.find_first_not_of('0'), current.size()-1));
    
    return {result.empty() ? "0" : result, current.empty() ? "0" : current};
}