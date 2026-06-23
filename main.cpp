#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

string split(const string& str){
    const string whitespace = " \t\n\r\f\v";
    size_t first = str.find_first_not_of(whitespace);
    if (first == string::npos) return "";
    size_t last = str.find_first_not_of(whitespace);
    return str.substr(first, (last - first + 1));
}

int main() {
    string code_line;
    vector<string> lines;
    vector<string> line;

    ifstream code("code.bas");

    while (getline (code, code_line)){
        lines.push_back(code_line);
    }

    code.close();

    cout << "Our code divided into single line: " << endl;
    for (const string& s : lines){
        cout << "Stored: " << s << endl;
    }

    
    for (const string& s : lines){
        string splited = split(s);
        line.push_back(splited);
    }

    cout << "Our striped lines:" << endl;
    for (const string& s : line){
        cout << "Splited: " << s << endl;
    }

    return 0;
}