import subprocess
import os

# List of directory prefixes
dir_pref = ['out', 'outLLVM', 'outQ']

# Define the path to the fuzzgoat binary compiled with ASAN
fuzzgoat_path = "./fuzzgoat_ASAN"

# Iterate over each directory prefix
for prefix in dir_pref:
    # Construct the path to the directory containing the crash files
    crashes_dir = f"{prefix}/default/crashes"
    
    # Initialize a dictionary to hold error names and their occurrences for the current directory
    error_counts = {}
    
    # Check if the crashes directory exists
    if not os.path.exists(crashes_dir):
        print(f"Directory {crashes_dir} does not exist. Skipping...")
        continue

    if(prefix=="out"):
    	print(f"\nProcessing GCC instrumented Fuzzgoat crashes")
    elif(prefix=="outLLVM"):
    	print(f"\nProcessing LLVM instrumented Fuzzgoat crashes")
    elif(prefix=="outQ"):
    	print(f"\nProcessing QEMU binary instrumented Fuzzgoat crashes")

    # Loop through each file in the crashes directory
    for crash_file in os.listdir(crashes_dir):
     # Skip README.txt
        if crash_file == "README.txt":
            continue
        crash_file_path = os.path.join(crashes_dir, crash_file)
        # Construct the command to run
        command = f"{fuzzgoat_path} {crash_file_path} 2>&1 | grep 'SUMMARY'"
        # Run the command and capture the output
        try:
            # Using shell=True to allow command pipelining and redirection
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            # Decode output and filter lines containing "SUMMARY"
            lines = output.decode('utf-8').splitlines()
            
            # Extract and count error names from summary lines
            for line in lines:
                # Split line to extract error name, which is the third element
                parts = line.split()
                error_name = parts[2]  # Assuming the error name is the third element
                # Increment count in dictionary
                error_counts[error_name] = error_counts.get(error_name, 0) + 1

        except subprocess.CalledProcessError as e:
            print(f"Error processing file {crash_file_path}: {e}")

    # Print unique error names and their occurrences for the current directory
    for error_name, count in error_counts.items():
        print(f"{error_name}: {count}")
