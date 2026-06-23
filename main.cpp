#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

vector<string> split(const string& str, const string& delimiter) {
    vector<string> tokens;
    size_t prev = 0, pos = 0;
    while ((pos = str.find(delimiter, prev)) != string::npos){
        tokens.push_back(str.substr(prev, pos - prev));
        prev = pos + delimiter.length();
    }
    tokens.push_back(str.substr(prev));
    return tokens;
}

int main() {
    string code_line;
    vector<string> lines;

    ifstream code("code.bas");

    while (getline (code, code_line)){
        lines.push_back(code_line);
    }
    code.close();

    cout << "Our code divided into single line: " << endl;
    for (const string& s : lines){
        cout << "Stored: " << s << endl;
    }

    for (const string& s : lines) {
        vector<string> splitted = split(s, " ");
        for (const string& token : splitted){
            cout << token;
        }
        cout << endl;
    }

    return 0;
}