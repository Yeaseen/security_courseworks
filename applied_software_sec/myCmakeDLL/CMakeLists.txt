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
