#include <iostream>
#include <string>
using namespace std;

string highestScoringWord(const string &str);

int main() {
	
cout << highestScoringWord("London is a capital of great Britain") << endl;
	
return 0;
}

string highestScoringWord(const string &str) {
	int max = 0, score = 0, len = str.length();
	string max_word = "", word = "";
	for(int i = 0; i < len + 1; i++) {
		if(str[i] != ' ' && i != len) {   
			word += str[i];
			score += tolower(str[i]) - 'a' + 1;
		}
		else {
			if(score > max) {
				max = score;
				max_word = word;
			}
		score = 0;
		word = "";
		}	     
	}
return max_word;
}