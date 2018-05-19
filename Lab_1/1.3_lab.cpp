#include <iostream>
#include <vector>

using namespace std;

class Kata
{
public:
    int countInversions(vector<int> array)
    {
      int counter = 0;
      for(int i = 0; i<array.size(); i++) {
        for(int j = i; j<array.size(); j++) {
          if(array[i] > array[j]) counter++;
        }
      }  
      return counter;
    }
};

int main() {

vector<int> vec(5);
vec.push_back(9);
vec.push_back(2);
vec.push_back(3);
vec.push_back(-8);
vec.push_back(4);
  
Kata one;
cout << one.countInversions(vec);  

return 0;
}