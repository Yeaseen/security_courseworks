This folder contains a cpp implementation of an abstract interpretation of a transfer function of llvm.

## How to compile and run the code:

```bash
# The following command will give path to the include header
llvm-config --includedir

# The following command will give path to the llvm library
llvm-config --libdir

# compile program.cpp
clang++ -std=c++17 -I/path/to/include -L/path/to/llvm/lib -lLLVM program.cpp -o program

./program <bitwidth>

# example run for bitwidth 6

./program 6
```

## Expected Output

```plaintext
After running, the program will display the precision comparison results, indicating which transfer function is more precise for the given bitwidth.
```


## Overview

This work implements and evaluates custom transfer functions in the LLVM abstract interpretation framework. We specifically work with integer ranges for a specified bitwidth and analyze the precision of two different methods for multiplying a range by a constant factor of 3.

## Steps and Explanation

### 1. **Setting Up the Bitwidth**
   - The code begins by allowing the user to specify a bitwidth (default is 4 if not provided). This bitwidth is used to define the range of integers we’re working with for abstract interpretation.

### 2. **Enumerating All Possible Ranges**
   - Using the specified bitwidth, the program enumerates all possible `ConstantRange` objects representing different integer intervals. This enumeration helps in testing and analyzing the precision of the custom transfer functions.

### 3. **Concretization and Abstraction Functions**
   - **Concretization**: Converts a `ConstantRange` into a set of `APInt` values, representing all integers within the specified range.
   - **Abstraction**: Uses the `abstractRange` function to find the smallest range containing a given set of values. This ensures that the results of transfer functions are generalized to the minimal range covering all potential values in that set.
   
### 4. **Transfer Functions for Multiplying by 3**
   - **Composite Transfer Function**: Multiplies the bounds of a range directly by 3.
   - **Decomposed Transfer Function**: Multiplies by 3 using a decomposition strategy:
     - Shifts the range left by 1 bit (equivalent to multiplying by 2).
     - Adds the original range to the shifted result.
   - These transfer functions demonstrate different ways of representing the same operation, with potential trade-offs in precision.

### 5. **Comparing Precision of Transfer Functions**
   - For each range, the program applies both transfer functions and evaluates their precision.
   - **Precision Evaluation**:
     - **Subset Check**: Uses the `abstractRange` function to re-abstract each result and then concretizes both for a set-based comparison.
     - **Composite vs. Decomposed Precision**: The comparison counts which function is more precise by checking if one result is a subset of the other.

### 6. **Results Summary**
   - The program outputs the total number of ranges tested and the count of cases where:
     - The composite transfer function is more precise.
     - The decomposed transfer function is more precise.
     - The results are incomparable (should ideally be zero).
   - This summary provides insight into the relative accuracy and reliability of each method.

## How LLVM Is Used

- **`ConstantRange` and `APInt`**: LLVM’s `ConstantRange` class is used to define and manipulate integer ranges, while `APInt` provides arbitrary-precision integer handling within these ranges.
- **`abstractRange`**: A custom abstraction function that takes advantage of `ConstantRange` to find the smallest interval that contains all values in a given set.
- **LLVM Utilities**: Functions like `toString`, `shl`, and `add` are LLVM utilities used for formatting, shifting, and arithmetic within `ConstantRange`.
