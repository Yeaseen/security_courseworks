#!/bin/bash

# Define where to clone and build libarchive
CLONE_DIR="/mnt/bigdata/YEASEEN/PG/Harnessing_libarchive/libarchive"
BUILD_DIR="${CLONE_DIR}/build"
INSTALL_DIR="${CLONE_DIR}/libarchive_install"

# Ensure the script exits on first error
set -e

# Step 1: Clone the libarchive repository
if [ ! -d "${CLONE_DIR}/libarchive" ]; then
    echo "Cloning libarchive repository..."
    git clone https://github.com/libarchive/libarchive.git "${CLONE_DIR}/libarchive"
else
    echo "libarchive repository already exists. Skipping clone."
fi

# Step 2: Create a build directory
echo "Creating build directory..."
mkdir -p "${BUILD_DIR}"

# Step 3: Set environment variables for AFL's compilers
export CC=/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast  # Adjust this path as necessary
export CXX=/mnt/bigdata/YEASEEN/PG/AFLPlusPlus/afl-clang-fast++  # Adjust this path as necessary

# Step 4: Run cmake from the build directory
echo "Running cmake with AFL's compilers..."
cd "${BUILD_DIR}"
cmake -DCMAKE_INSTALL_PREFIX="${INSTALL_DIR}" ../libarchive

# Step 5: Build libarchive
echo "Building libarchive with AFL's instrumentation..."
make -j$(nproc)

# Step 6: Install libarchive locally
echo "Installing libarchive locally..."
make install

echo "libarchive has been successfully built and installed to ${INSTALL_DIR}."
