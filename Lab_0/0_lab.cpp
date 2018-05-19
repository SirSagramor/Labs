#include <iostream>
using namespace std;

char matrix[26][26];
string str, key, answer;

int main(){
    cout << "Write your line, please\n";
    cin >> str;
    cout << "Write your key, please\n";
    cin >> key;
    for (int i = 0; i < 26; i++){
        for (int j = 0; j <= i; j++){
            matrix[i][j] = (i + j) % 26 + 97;
            matrix[j][i] = matrix[i][j];
        }
    }
   for (int i = 0; i < str.length(); i++){
        const int ch = str[i] - '0' - 49;
        if (ch >= 0 && ch < 26) {
            answer += matrix[ch][key[i % key.length()] - '0' - 49];
        }
    }
    cout << "Cipher is: " << answer << endl;
}

