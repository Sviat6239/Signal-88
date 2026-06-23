#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {

    string code_line;

    ifstream code("code.bas");

    while (getline (code, code_line)){
        cout << code_line << endl;
    }

    code.close();

    return 0;
}