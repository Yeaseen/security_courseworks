
# C++ Project Setup with CMake

This document describes the setup for a simple C++ project using CMake. The project consists of a  file (`file.cpp`), a header file (`file.h`), another header file (`file1.h`), and an additional cpp file (`file1.cpp`). Now, a shared object library file named `libMyLibrary.so` will be created from the CMakeLists file. You have to load the library file's location. Then, you would be able to use its functions described in the header files.

## Project Structure

```plaintext
project/
│
├── CMakeLists.txt
├── file.h
├── file.cpp
├── file1.h
├── file1.cpp
└── myTest.cpp

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


## CMakeLists.txt

This CmakeLists is to build your cpp files and finally to have the shared object file to be used by others.

```cmake
cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(MyProject VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Instead of add_executable, use add_library to create a shared library
add_library(MyLibrary SHARED file.cpp file1.cpp)

# Optionally, set properties for your library
set_target_properties(MyLibrary PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER "file.h;file1.h"
)

# Optionally set the install directory for the library
install(TARGETS MyLibrary
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include
)
```

## Building and Testing

To build and use your shared library, follow these steps:

1. **Create a build directory** and navigate into it:
   ```shell
   mkdir build && cd build
   ```

2. **Configure the project with CMake**:
   ```shell
   cmake ..
   ```

3. **Build the project with Make**:
   ```shell
   make
   ```
After building your project, you can delete the cpp files. You just need the header files and the shared object file. Also, installation step is optional. If you just build, you will be haveing `MyLibrary` so file inside the build driectory.

4. Setup environment variable for loading that library.
   ```shell
    export LD_LIBRARY_PATH=/path/to/your/build/directory/:$LD_LIBRARY_PATHD
   ```
5. Now write a test cpp file to use that shared library file. You just need to put the header file names.

```cpp
#include "file.h"
#include "file1.h"

int main() {
    printMessage();
    printAnotherMessage();
    return 0;
}
```

6. Compile this cpp file by providing the library path and the shared object file name.
    
    ```shell
    g++ -o MyTest myTest.cpp -L/path/to/your/build/directory/ -lMyLibrary
   ```
7. Finally run the created object file.

    ```shell
    ./MyTest
   ```


