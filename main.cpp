#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

#include "llvm/CodeGen/Passes.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Analysis/TargetTransformInfo.h"

#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Function.h"

using namespace std;
using namespace llvm;

int main() {
    vector<vector<string>> code_lines;
    vector<string> int_variables;
    vector<string> str_variables;

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
        if (row[0] == 'let'){

        }
    }

    return 0;
}