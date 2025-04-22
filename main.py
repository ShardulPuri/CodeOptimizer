# main.py - Main script for the Code Optimizer

import os
import sys
import argparse
from pathlib import Path

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the project root to the Python path
sys.path.append(script_dir)

try:
    from parser.parser import process_file
    from tac_utils.formatter import print_tac
    from tac_utils.io import save_tac_to_file
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

def main():
    """
    Main function to run the TAC generator.
    """
    parser = argparse.ArgumentParser(description='Generate Three-Address Code (TAC) from C code.')
    
    # Use relative paths based on script location
    default_input = os.path.join(script_dir, 'input', 'sample.c')
    default_output = os.path.join(script_dir, 'output', 'tac_output.txt')
    
    parser.add_argument('-i', '--input', default=default_input, help='Input C file')
    parser.add_argument('-o', '--output', default=default_output, help='Output TAC file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Get absolute paths
    input_file = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output)
    
    if args.verbose or args.debug:
        print(f"Script directory: {script_dir}")
        print(f"Processing file: {input_file}")
        print(f"Output file: {output_file}")
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        # Show directory structure for debugging
        if args.debug:
            print("\nProject Directory Structure:")
            for root, dirs, files in os.walk(script_dir):
                level = root.replace(script_dir, '').count(os.sep)
                indent = ' ' * 4 * level
                print(f"{indent}{os.path.basename(root)}/")
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    print(f"{sub_indent}{f}")
        return 1
    
    # Process the input file
    try:
        tac_instructions = process_file(input_file)
    except Exception as e:
        print(f"Error during processing: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    
    if not tac_instructions:
        print("No TAC instructions generated. This could be due to:")
        print("1. The parser couldn't understand the C code")
        print("2. The C code didn't contain any supported operations")
        print("3. There was an error in the TAC generation process")
        print("\nTry running with --debug flag for more information.")
        return 1
    
    # Print the TAC instructions if verbose
    if args.verbose or args.debug:
        print("\nGenerated TAC:")
        print_tac(tac_instructions)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the TAC instructions to a file
    try:
        if save_tac_to_file(tac_instructions, output_file):
            print(f"\nTAC successfully saved to {output_file}")
            print(f"Raw TAC saved to {Path(output_file).with_suffix('.json')}")
        else:
            print("Failed to save TAC to file.")
            return 1
    except Exception as e:
        print(f"Error saving TAC: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())