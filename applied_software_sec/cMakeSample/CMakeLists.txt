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
