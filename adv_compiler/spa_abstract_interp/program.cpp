#include "llvm/IR/ConstantRange.h"
#include "llvm/ADT/APInt.h"
#include "llvm/Support/raw_ostream.h"
#include <vector>
#include <iostream>
#include <algorithm>
#include <set>
#include <cstdlib> // For atoi
using namespace llvm;
using namespace std;



// Function to enumerate all possible valid integer ranges for the 4-bit width
vector<ConstantRange> enumerateAllRanges(unsigned int bitwidth) {
    vector<ConstantRange> ranges;
    // Loop through all possible start points
    for (unsigned start = 0; start < (1 << bitwidth); ++start) {
        for (unsigned end = start; end < (1 << bitwidth); ++end) {
            APInt lower(bitwidth, start);
            APInt upper(bitwidth, end + 1); // end is inclusive
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
ConstantRange abstractRange(const vector<APInt> &values, unsigned int bitwidth) {
    if (values.empty()) {
        return ConstantRange(APInt(bitwidth, 0), APInt(bitwidth, 0));
    }

    APInt minValue = findMinAPInt(values);
    APInt maxValue = findMaxAPInt(values) + 1; // Upper bound is exclusive

    return ConstantRange(minValue, maxValue);
}


// Composite transfer function that multiplies the range by 3
ConstantRange multiplyBy3(const ConstantRange &range) {
    APInt lower = range.getLower() * 3;
    APInt upper = range.getUpper() * 3;
    return ConstantRange(lower, upper);
}

// Decomposed transfer function for multiplication by 3
ConstantRange decomposedMultiplyBy3(const ConstantRange &range) {
    // Step 1: Shift both bounds of the range left by 1 bit (multiply by 2)
    APInt shiftedLower = range.getLower().shl(1);
    APInt shiftedUpper = range.getUpper().shl(1);
    ConstantRange shiftedRange(shiftedLower, shiftedUpper);

    // Step 2: Add the original range to the shifted range
    ConstantRange resultRange = shiftedRange.add(range);

    return resultRange;
}


// Helper function to print the bounds of a ConstantRange
void printRange(const ConstantRange &range) {
    SmallString<16> lowerStr, upperStr;
    range.getLower().toString(lowerStr, 10, false);
    range.getUpper().toString(upperStr, 10, false);
    llvm::outs() << "[" << lowerStr << ", " << upperStr << ")\n";
}


// Helper function to convert a vector of APInts to a set of integers for easy comparison
std::set<uint64_t> toSet(const std::vector<APInt> &values) {
    std::set<uint64_t> resultSet;
    for (const auto &val : values) {
        resultSet.insert(val.getZExtValue());
    }
    return resultSet;
}


int main(int argc, char *argv[]) {
    // Set default bitwidth
    unsigned int bitwidth = 4;

    // If a command-line argument is provided, use it as the bitwidth
    if (argc > 1) {
        bitwidth = std::atoi(argv[1]);
    }


    // Enumerate all ranges and print them
    vector<ConstantRange> ranges = enumerateAllRanges(bitwidth);
    //llvm::outs() << "The Ranges:\n";
    //printRanges(ranges);



    // Test concretization on a sample range
    // ConstantRange sampleRange(APInt(bitwidth, 3), APInt(bitwidth, 8)); // Range [3, 8)
    // llvm::outs() << "Concretized values for range [3, 8): ";
    // vector<APInt> concretizedValues = concretizeRange(sampleRange);
    // printConcretizedValues(concretizedValues);

     // Test abstraction on the concretized values
    // ConstantRange abstractedRange = abstractRange(concretizedValues, bitwidth);
    // SmallString<16> lowerStr, upperStr;
    // abstractedRange.getLower().toString(lowerStr, 10, false);
    // abstractedRange.getUpper().toString(upperStr, 10, false);
    // llvm::outs() << "Abstracted range for values {3, 4, 5, 6, 7}: [" 
    //              << lowerStr << ", " << upperStr << ")\n";


    // ConstantRange multipliedRange = multiplyBy3(sampleRange);
    // llvm::outs() << "Range after multiplying by 3: ";
    // printRange(multipliedRange);


     // Apply decomposed transfer function
    // ConstantRange decomposedRange = decomposedMultiplyBy3(sampleRange);
    // llvm::outs() << "Range after decomposed multiply by 3: ";
    // printRange(decomposedRange);


    // Initialize counters
    int totalAbstractValues = 0;
    int compositeMorePrecise = 0;
    int decomposedMorePrecise = 0;
    int incomparableResults = 0;

     // Exhaustively test each range
for (const auto &range : ranges) {
    totalAbstractValues++;

    // Apply composite and decomposed transfer functions
    ConstantRange compositeResult = multiplyBy3(range);
    ConstantRange decomposedResult = decomposedMultiplyBy3(range);

    // Concretize both ranges and then re-abstract them
    ConstantRange compositeAbstracted = abstractRange(concretizeRange(compositeResult), bitwidth);
    ConstantRange decomposedAbstracted = abstractRange(concretizeRange(decomposedResult), bitwidth);

    // Convert the abstracted ranges to sets of values for comparison
    std::set<uint64_t> compositeSet = toSet(concretizeRange(compositeAbstracted));
    std::set<uint64_t> decomposedSet = toSet(concretizeRange(decomposedAbstracted));

    // Determine relationships between the sets
    bool compositeIsSubset = std::includes(decomposedSet.begin(), decomposedSet.end(),
                                           compositeSet.begin(), compositeSet.end());
    bool decomposedIsSubset = std::includes(compositeSet.begin(), compositeSet.end(),
                                            decomposedSet.begin(), decomposedSet.end());

    if (compositeIsSubset && !decomposedIsSubset) {
        compositeMorePrecise++;
    } else if (decomposedIsSubset && !compositeIsSubset) {
        decomposedMorePrecise++;
    } else if (!compositeIsSubset && !decomposedIsSubset) {
        incomparableResults++;
    }
}     // Report results
    llvm::outs() << "Total abstract values tested: " << totalAbstractValues << "\n";
    llvm::outs() << "Composite more precise: " << compositeMorePrecise << "\n";
    llvm::outs() << "Decomposed more precise: " << decomposedMorePrecise << "\n";
    llvm::outs() << "Incomparable results: " << incomparableResults << "\n";

    return 0;
}
