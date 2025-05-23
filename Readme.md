# Code Optimizer - Three-Address Code Generator

This project implements a tool that converts C code into Three-Address Code (TAC) representation, which can be used for compiler optimization techniques.

## Project Structure

```
CodeOptimizer/
├── input/
│   └── sample.c                # Sample C input file
├── parser/
│   └── parser.py               # Use pycparser to extract TAC
├── tac_utils/
│   ├── formatter.py            # Functions to print and format TAC
│   └── io.py                   # Load/save TAC from/to file
├── output/
│   └── tac_output.txt          # Store generated TAC
└── main.py                     # Main script
```

## Requirements

- Python 3.6+
- pycparser

## Installation

1. Install the required packages:

```bash
pip install pycparser
```

2. Clone this repository or download the source code.

## Usage

Run the main script to generate TAC from a C file:

```bash
python main.py -i input/sample.c -o output/tac_output.txt
```

Options:
- `-i, --input`: Input C file (default: input/sample.c)
- `-o, --output`: Output TAC file (default: output/tac_output.txt)
- `-v, --verbose`: Print verbose output

## Three-Address Code (TAC) Format

The TAC is represented as a list of instructions in Python dictionaries:

1. Assignment: `{'type': 'assign', 'lhs': 'a', 'rhs': '5'}`
2. Binary Operation: `{'type': 'binop', 'lhs': 't0', 'op': '+', 'arg1': 'a', 'arg2': 'b'}`
3. Unary Operation: `{'type': 'unaryop', 'lhs': 't1', 'op': '-', 'arg': 'a'}`

The output file contains a human-readable representation of the TAC, and a JSON file with the raw TAC data is also generated for machine processing.

## Current Limitations

- Only supports basic constructs: variable declarations, assignments, and binary operations
- Does not handle control flow structures (if, while, etc.) yet
- Does not handle function calls or definitions yet

## Future Work

This is Phase 1 of the project. Future phases will implement:
- Support for more complex C constructs
- Optimization techniques on the generated TAC
- Code generation from optimized TAC

## License

This project is open-source and available under the MIT License.#   C o d e O p t i m i z e r  
 