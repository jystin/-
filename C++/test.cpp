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

bool isShorter(const Person &, const Person &);

vector<int>* add_vector(vector<int>, vector<int>);

int main() {
    vector<int> v1 = {1, 2, 3};
    vector<int> v2 = {4, 5, 6};
    vector<int> *pv = add_vector(v1, v2);
    for (int i = 0; i < pv->size(); i++) {
        cout << (*pv)[i] << " ";
    }

}

bool isShorter(const Person &p1, const Person &p2) {
    return p1.height < p2.height;
}

vector<int>* add_vector(vector<int> v1, vector<int> v2) {
    vector<int> *pv = new vector<int>;
    for (int i = 0; i < v1.size(); i++) {
        pv->push_back(v1[i] + v2[i]);
    }
    return pv;
}