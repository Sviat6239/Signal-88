#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main() {
    vector<vector<string>> code_lines;

    ifstream f("code.bas");
    string line;

    if (f.is_open()){
        while (getline(f, line)){
            if(!line.empty()){
                vector<string> parts;
                stringstream ss(line);
                string word;

                while (ss >> word){
                    parts.push_back(word);
                }

                if (!parts.empty()){
                    code_lines.push_back(parts);
                }
            }
        }
        f.close();
    }

    for (const auto& row : code_lines){
        for (const auto& word : row){
            cout << word << " ";
        }
        cout << endl;
    }

    return 0;
}