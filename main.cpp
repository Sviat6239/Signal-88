//std includes
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <unordered_map>
#include <map>
#include <set>
#include <stack>

//llvm includes
#include "llvm/CodeGen/Passes.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Analysis/TargetTransformInfo.h"

//llvm IR includes
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Function.h"

//namespaces
using namespace std;
using namespace llvm;

//entry poin - main function
int main() {
    vector<vector<string>> code_lines;
    vector<vector<string>> output;

    map<string, string> int_variables;
    map<string, string> str_variables;

    set<string> needed_functions;
    set<string> needed_constants;

    int temp_buffer_count = 0;
    int str_to_print_count = 0;
    int if_label_count = 0;

    stack<int> if_stac;

    map<string, string> string_buffers;

    unordered_map<string, string> functions = {

    };

    unordered_map<string, string> constants = {

    };

    //llvm content init
    LLVMContext context;
    Module* module = new Module("basic_module", context);
    IRBuilder<> builder(context);

    FunctionType* funcType = FunctionType::get(builder.getInt32Ty(), false);
    Function* mainFunc = FUnction::Create(FuncType, Function::ExternalLinkage, "main", module);
    BasicBlock* entry = BasicBlock::Create(context, "entry", mainFunc);
    builder.SetInsertPoint(entry);

    //reading file
    ifstream f("code.bas");
    string line;

    //tokenizer
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

    //main loop
    for (const auto& row : code_lines){
        if (row[0] == 'let'){

        } else if (row[0] == 'add'){

        } else if (row[0] == 'sub'){

        } else if (row[0] == 'mul'){

        } else if (row[0] == 'div'){

        } else if (row[0] == 'sqr'){

        } else if (row[0] == 'root'){

        } else if (row[0] == 'pow'){

        } else if (row[0] == 'log'){

        } else if (row[0] == 'log10'){

        } else if (row[0] == 'sin'){

        } else if (row[0] == 'cos'){

        } else if (row[0] == 'tg'){

        } else if (row[0] == 'ctg'){

        } else if (row[0] == 'arc-sin'){

        } else if (row[0] == 'arc-cos'){

        } else if (row[0] == 'arc-tg'){

        } else if (row[0] == 'arc-ctg'){

        } else if (row[0] == 'fact'){

        } else if (row[0] == 'tetr'){

        } else if (row[0] == 'mov'){

        } else if (row[0] == 'print'){

        } else if (row[0] == 'prtln'){

        } else if (row[0] == 'read'){

        } else if (row[0] == 'tostr'){

        } else if (row[0] == 'toint'){

        } else if (row[0] == 'tobin'){

        } else if (row[0] == 'tohex'){

        } else if (row[0] == 'tooct'){

        } else if (row[0] == 'tostrbin'){

        } else if (row[0] == 'tostrhex'){

        } else if (row[0] == 'tostroct'){

        } else if (row[0] == 'if'){

        } else if (row[0] == 'elif'){

        } else if (row[0] == 'else'){

        } else if (row[0] == 'end'){

        } else if (row[0] == 'label'){

        } else if (row[0] == 'jmp'){

        } else if (row[0] == 'jne'){

        } else if (row[0] == 'je'){

        } else if (row[0] == 'jge'){

        } else if (row[0] == 'jg'){

        } else if (row[0] == 'jle'){

        } else if (row[0] == 'jl'){

        } else if (row[0] == 'cmp'){

        } else if (row[0] == 'struct'){

        } else if (row[0] == 'call'){

        } else if (row[0] == 'apicall'){

        } else if (row[0] == 'syscall'){

        }

    }

    return 0;
}