$llvm_flags = llvm-config --cxxflags --ldflags --libs Core Support
clang++ main.cpp -o my_app.exe $llvm_flags