# io.py - Load/save TAC from/to file

import json
import os
from pathlib import Path

def save_tac_to_file(instructions, output_file):
    """
    Save TAC instructions to a file.
    
    Args:
        instructions (list): List of TAC instructions
        output_file (str): Path to the output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create the directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Import the formatter properly using relative import
        from tac_utils.formatter import format_tac
        formatted_tac = format_tac(instructions)
        
        # Write formatted TAC to text file
        with open(output_file, 'w') as f:
            f.write(formatted_tac)
        
        # Save raw instructions in JSON format for potential machine processing
        json_file = Path(output_file).with_suffix('.json')
        with open(json_file, 'w') as f:
            json.dump(instructions, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving TAC to file: {e}")
        return False

def load_tac_from_file(input_file):
    """
    Load TAC instructions from a JSON file.
    
    Args:
        input_file (str): Path to the input file (should be a .json file)
        
    Returns:
        list: List of TAC instructions, or empty list if loading fails
    """
    try:
        # Check if the file exists
        if not os.path.exists(input_file):
            print(f"Error: File {input_file} not found.")
            return []
        
        # Load instructions from JSON file
        with open(input_file, 'r') as f:
            instructions = json.load(f)
            
        return instructions
    except json.JSONDecodeError:
        print(f"Error: File {input_file} is not valid JSON.")
        return []
    except Exception as e:
        print(f"Error loading TAC from file: {e}")
        return []

if __name__ == "__main__":
    # Example TAC instructions for testing
    example_tac = [
        {'type': 'assign', 'lhs': 'a', 'rhs': '5'},
        {'type': 'assign', 'lhs': 'b', 'rhs': '7'},
        {'type': 'binop', 'lhs': 't0', 'op': '+', 'arg1': 'a', 'arg2': 'b'},
        {'type': 'assign', 'lhs': 'c', 'rhs': 't0'},
    ]
    
    # Save the example to a file
    test_output = "../output/test_tac.txt"
    save_tac_to_file(example_tac, test_output)
    
    print(f"Example TAC saved to {test_output}")
    print(f"Raw TAC saved to {Path(test_output).with_suffix('.json')}")