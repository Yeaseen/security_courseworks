
# C++ Project Setup with CMake

This document describes the setup for a simple C++ project using CMake. The project consists of a  file (`file.cpp`), a header file (`file.h`), another header file (`file1.h`), and an additional cpp file (`file1.cpp`). The main code is in`driver.cpp` file. The final output will be an executable named `MyExecutable` based on the `driver.cpp` file.

## Project Structure

```plaintext
project/
│
├── CMakeLists.txt
├── file.h
├── file.cpp
├── file1.h
├── file1.cpp
└── driver.cpp

```

### file.h

```cpp
#ifndef FILE_H
#define FILE_H

void printMessage();

#endif // FILE_H
```

### file.cpp

```cpp
#include "file.h"
#include <iostream>

void printMessage() {
    std::cout << "Hello from file.cpp!" << std::endl;
}
```

### file1.h

```cpp
#ifndef FILE1_H
#define FILE1_H

void printAnotherMessage();

#endif // FILE1_H
```

### file1.cpp

```cpp
#include "file1.h"
#include <iostream>

void printAnotherMessage() {
    std::cout << "Hello from file1.cpp!" << std::endl;
}
```

### driver.cpp
```cpp
#include "file.h"
#include "file1.h"
#include <iostream>


int main() {
    printMessage();
    printAnotherMessage();
    return 0;
}
```

## CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(MyProject VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add executable target with source files
add_executable(MyExecutable driver.cpp file.cpp file1.cpp)

# Optionally set the install directory
install(TARGETS MyExecutable DESTINATION bin)
```

## Building and Installing

To build and install your project, follow these steps:

1. **Create a build directory** and navigate into it:
   ```shell
   mkdir build && cd build
   ```

2. **Configure the project with CMake**:
   ```shell
   cmake -DCMAKE_INSTALL_PREFIX=../install_ ..
   ```

3. **Build the project with Make**:
   ```shell
   make
   ```

4. **Install the project** (might require `sudo` depending on the install destination):
   ```shell
   make install
   ```

After these steps, the executable `MyExecutable` will be compiled and installed to the specified `bin` directory.