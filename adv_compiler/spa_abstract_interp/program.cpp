#include "llvm/IR/ConstantRange.h"
#include "llvm/ADT/APInt.h"
#include "llvm/Support/raw_ostream.h"
#include <vector>
#include <iostream>

using namespace llvm;
using namespace std;

// Define a constant for the bitwidth
const unsigned int BITWIDTH = 4;

// Function to enumerate all possible valid integer ranges for the 4-bit width
vector<ConstantRange> enumerateAllRanges() {
    vector<ConstantRange> ranges;
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

int main() {
    // Enumerate all ranges and print them
    vector<ConstantRange> ranges = enumerateAllRanges();
    llvm::outs() << "The Ranges:\n";
    printRanges(ranges);

    return 0;
}
