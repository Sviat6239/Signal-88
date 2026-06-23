#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main() {
    string code_line;
    vector<string> lines;

    ifstream code("code.bas");

    while (getline (code, code_line)){
        lines.push_back(code_line);
    }

    code.close();

    for (const string& s : lines){
        cout << "Stored: " << s << endl;
    }

    return 0;
}