#include <iostream>
#include <string>
#include <vector>
#include <iterator>
using namespace std;

class Kata {
public:
	vector<string> towerBuilder(const int &nFloors) {
		const int center = nFloors - 1;
		string floor(2 * nFloors - 1, ' ');
		vector<string> vec;
		
		for(int i = 0; i <= center; ++i) {
			floor.replace(center + i, 1, "*");
			floor.replace(center - i, 1, "*");
			vec.push_back(floor);
		}
		return vec;
	}
};

int main() {

Kata kata;
vector<string> actual = kata.towerBuilder(61);
copy(actual.begin(), actual.end(),  ostream_iterator<string>(cout, "\n"));

return 0;
}


