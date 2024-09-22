# Writing an LLVM Pass

This README details the steps for writing an LLVM pass that adds an `-O2` level optimization. The merged PR can be found [here](https://github.com/regehr/llvm-project/pull/59).

## Prerequisites

Before starting, ensure you have the following installed:

- CMake
- Ninja
- Clang
- Git

### macOS M1 Users

If you are on an Apple M1 system, you can install these tools using Homebrew:

```bash
brew install cmake ninja re2c git
```

## Step 1: Cloning and Building LLVM

First, clone the LLVM repository and check out the branch for the assignment.

```bash
git clone https://github.com/regehr/llvm-project
cd llvm-project
git checkout cs6475-assignment2
```

Next, create a build directory and configure the build using CMake.

```bash
mkdir build
cd build
cmake -GNinja -DLLVM_ENABLE_RTTI=ON -DLLVM_ENABLE_EH=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_ASSERTIONS=ON -DLLVM_ENABLE_PROJECTS="llvm;clang" ../llvm -DBUILTINS_CMAKE_ARGS=-DCOMPILER_RT_ENABLE_IOS=OFF
```

Now, build LLVM using Ninja.

```bash
cmake --build . --parallel
```

This may take some time depending on your system's hardware.

## Step 2: Writing an LLVM IR Program

Navigate to the `build` directory and create an LLVM IR file named `src.ll`. This file will contain the LLVM IR code that you want to optimize. Here is a basic example of an LLVM IR function:

```llvm
; src.ll
define i16 @example(i16 %x) {
  %a = xor i16 %x, 3333
  %b = sub i16 32767, %a
  ret i16 %b
}
```

## Step 3: Running the Optimization Pass

Use the `opt` tool provided by LLVM to apply the `-O2` optimization pass to your LLVM IR code.

```bash
./bin/opt -O2 src.ll -S -o -
```

This command runs the `-O2` optimization level on `src.ll` and outputs the optimized LLVM IR to the terminal.

## Step 4: Getting Upstream Changes

To ensure your branch is up-to-date with the latest changes, pull from the upstream repository.

```bash
git pull origin cs6475-assignment2
```

If there are any merge conflicts, resolve them manually.

## Step 5: Creating a New Branch

Create a new branch for your modifications.

```bash
git checkout -b yeaseen-assignment2
```

## Step 6: Modifying the LLVM Pass

Modify the file `llvm/lib/Transforms/InstCombine/InstructionCombining.cpp` to add your optimization pass. This is where you'll write the code for your optimization.

For example, an optimization that transforms `MaxSignedValue - (x ⊕ c)` into `x ⊕ (MaxSignedValue - c)` could look like this:

```cpp
if (match(I, m_Sub(m_ConstantInt(C1), m_Xor(m_Value(X), m_ConstantInt(C2))))) {
    if (C1->getUniqueInteger().isMaxSignedValue()) {
        auto MaxSignedValue = APInt::getSignedMaxValue(C1->getUniqueInteger().getBitWidth());
        auto NewConstant = MaxSignedValue - C2->getValue();
        Instruction *NewI = BinaryOperator::CreateXor(X, ConstantInt::get(I->getContext(), NewConstant));
        return NewI;
    }
}
```

## Step 7: Rebuilding LLVM

After modifying the code, rebuild LLVM to incorporate your changes.

```bash
cmake --build . --parallel
```

## Step 8: Adding and Running Test Cases

Add your test cases to ensure the optimization works correctly. Place your tests in the file `llvm/test/Transforms/InstCombine/max_signed_value_xor.ll`.

### Example Test Case

```llvm
; RUN: opt -O2 -S < %s | FileCheck %s

define i16 @opt16(i16 %x) {
  ; CHECK-LABEL: @opt16(
  ; CHECK-NEXT: %b = xor i16 %x, 29434
  ; CHECK-NEXT: ret i16 %b
  %a = xor i16 %x, 3333
  %b = sub i16 32767, %a
  ret i16 %b
}
```

### Running the Test Case

Use `llvm-lit` to run your test file and verify that the optimization works as expected.

```bash
./bin/llvm-lit ../llvm/test/Transforms/InstCombine/max_signed_value_xor.ll
```

Ensure all tests pass before proceeding.

## Step 9: Creating the Pull Request

Once you have verified that your changes work correctly and pass all tests, push your branch to your fork on GitHub.

```bash
git push origin yeaseen-assignment2
```

Then, go to your GitHub repository and create a Pull Request (PR) to merge your changes into the upstream repository. Follow the steps:

1. Go to your fork on GitHub.
2. Click on **Compare & pull request**.
3. Fill in the title and description of your PR.
4. Submit the PR.

## Conclusion

You've successfully written and integrated an LLVM optimization pass. This process involves setting up the LLVM build environment, modifying source code, testing, and finally creating a pull request to merge your changes into the main repository.

If you encounter any issues or have questions, refer to the LLVM documentation or reach out to the LLVM community for support.
