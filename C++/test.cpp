#include <iostream>
#include <vector>
#include <array>
#include <string>
#include <cstring>
#include <ctime>
#include <cctype>
using namespace std;
const int Foot2inch = 12;

struct Person {
    string name;
    double height;
    double weight;
    int age = 2; // 有默认值的放在最后
    union
    {
        long long_id = 0;
        // string short_id = "000";
    };
};

enum color{red, green, blue};

typedef char APM;


int main() {
    int a;
    cin >> a;
    cout << a << endl;

}
