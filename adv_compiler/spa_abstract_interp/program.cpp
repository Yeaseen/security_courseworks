#include "llvm/IR/ConstantRange.h"
#include "llvm/ADT/APInt.h"
#include "llvm/Support/raw_ostream.h"
#include <vector>
#include <iostream>
#include <algorithm>

using namespace llvm;
using namespace std;

// Define a constant for the bitwidth
const unsigned int BITWIDTH = 4;

// Function to enumerate all possible valid integer ranges for the 4-bit width
vector<ConstantRange> enumerateAllRanges() {
    vector<ConstantRange> ranges;
    // Loop through all possible start points
    for (unsigned start = 0; start < (1 << BITWIDTH); ++start) {
        for (unsigned end = start; end < (1 << BITWIDTH); ++end) {
            APInt lower(BITWIDTH, start);
            APInt upper(BITWIDTH, end + 1); // end is inclusive
            ConstantRange range(lower, upper);
            ranges.push_back(range);
        }
    }
    return ranges;
}


void printRanges(const vector<ConstantRange> &ranges) {
    for (const auto &range : ranges) {
        SmallString<16> lowerStr, upperStr;
        range.getLower().toString(lowerStr, 10, false); // Base 10, unsigned
        range.getUpper().toString(upperStr, 10, false); // Base 10, unsigned
        llvm::outs() << "Range: [" << lowerStr << ", " << upperStr << ")\n";
    }
}

// Concretization function to get all values within a range
vector<APInt> concretizeRange(const ConstantRange &range) {
    vector<APInt> values;
    APInt current = range.getLower();
    APInt upper = range.getUpper();
    
    // Iterate from the lower bound up to (but not including) the upper bound
    while (current.ult(upper)) { // current < upper (for unsigned comparison)
        values.push_back(current);
        current = current + 1; // Increment the current value
    }
    
    return values;
}

// Helper function to print APInt values in concretized form
void printConcretizedValues(const vector<APInt> &values) {
    llvm::outs() << "{ ";
    for (const auto &val : values) {
        SmallString<16> str;
        val.toString(str, 10, false); // Convert to string in base 10, unsigned
        llvm::outs() << str << " ";
    }
    llvm::outs() << "}\n";
}


// Custom function to find minimum APInt in a vector
APInt findMinAPInt(const vector<APInt> &values) {
    APInt minValue = values[0];
    for (const auto &val : values) {
        if (val.ult(minValue)) {
            minValue = val;
        }
    }
    return minValue;
}

// Custom function to find maximum APInt in a vector
APInt findMaxAPInt(const vector<APInt> &values) {
    APInt maxValue = values[0];
    for (const auto &val : values) {
        if (maxValue.ult(val)) {
            maxValue = val;
        }
    }
    return maxValue;
}

// Abstraction function to get the smallest range containing all values in the set
ConstantRange abstractRange(const vector<APInt> &values) {
    if (values.empty()) {
        return ConstantRange(APInt(BITWIDTH, 0), APInt(BITWIDTH, 0));
    }

    APInt minValue = findMinAPInt(values);
    APInt maxValue = findMaxAPInt(values) + 1; // Upper bound is exclusive

    return ConstantRange(minValue, maxValue);
}




int main() {
    // Enumerate all ranges and print them
    vector<ConstantRange> ranges = enumerateAllRanges();
    //llvm::outs() << "The Ranges:\n";
    //printRanges(ranges);


    // Test concretization on a sample range
    ConstantRange sampleRange(APInt(BITWIDTH, 3), APInt(BITWIDTH, 8)); // Range [3, 8)
    llvm::outs() << "Concretized values for range [3, 8): ";
    vector<APInt> concretizedValues = concretizeRange(sampleRange);
    printConcretizedValues(concretizedValues);

     // Test abstraction on the concretized values
    ConstantRange abstractedRange = abstractRange(concretizedValues);
    SmallString<16> lowerStr, upperStr;
    abstractedRange.getLower().toString(lowerStr, 10, false);
    abstractedRange.getUpper().toString(upperStr, 10, false);
    llvm::outs() << "Abstracted range for values {3, 4, 5, 6, 7}: [" 
                 << lowerStr << ", " << upperStr << ")\n";

    

    return 0;
}
