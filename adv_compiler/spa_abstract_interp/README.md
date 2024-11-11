This folder contains a cpp implementation of an abstract interpretation of a transfer function of llvm.

## How to compile and run the code:

```bash
# The following command will give path to the include header
llvm-config --includedir

# The following command will give path to the llvm library
llvm-config --libdir

# compile program.cpp
clang++ -std=c++17 -I/path/to/include -L/path/to/llvm/lib -lLLVM program.cpp -o program


./program
```
