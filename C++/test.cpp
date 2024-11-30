#include <iostream>
#include <vector>
#include <array>
#include <string>
#include <cstring>
#include <ctime>
#include <cctype>
#include <cmath>
using namespace std;

struct polar {
    double distance;
    double angle;
};

struct rect {
    double x;
    double y;
};

polar rect_to_polar(rect xypos) {
    polar answer;
    answer.distance = sqrt(xypos.x * xypos.x + xypos.y * xypos.y);
    answer.angle = atan2(xypos.y, xypos.x);
    return answer;
}

void show_polar(polar dapos) {
    const double Rad_to_deg = 57.29577951;
    cout << "distance = " << dapos.distance;
    cout << ", angle = " << dapos.angle * Rad_to_deg;
    cout << " degrees\n";
}

void show_plar2(const polar *dapos);

int main() {
    int * list [5] = {1, 2, 3, 4, 5};
    cout << list[0] << endl;
}

void show_plar2(const polar *dapos)
{
    const double Rad_to_deg = 57.29577951;
    cout << "distance = " << dapos->distance;
    cout << ", angle = " << dapos->angle * Rad_to_deg;
    cout << " degrees\n";
}
