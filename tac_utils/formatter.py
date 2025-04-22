# formatter.py - Functions to print and format TAC

def format_instruction(instruction):
    """
    Format a single TAC instruction into a readable string.
    
    Args:
        instruction (dict): The TAC instruction to format
        
    Returns:
        str: A readable string representation of the instruction
    """
    if instruction['type'] == 'assign':
        return f"{instruction['lhs']} = {instruction['rhs']}"
    
    elif instruction['type'] == 'binop':
        return f"{instruction['lhs']} = {instruction['arg1']} {instruction['op']} {instruction['arg2']}"
    
    elif instruction['type'] == 'unaryop':
        return f"{instruction['lhs']} = {instruction['op']}{instruction['arg']}"
    
    elif instruction['type'] == 'label':
        return f"L{instruction['label']}:"
    
    elif instruction['type'] == 'jump':
        return f"goto L{instruction['target']}"
    
    elif instruction['type'] == 'cond_jump':
        return f"if {instruction['condition']} goto L{instruction['target']}"
    
    else:
        return str(instruction)  # Default case for unknown instruction types

def format_tac(instructions):
    """
    Format a list of TAC instructions into a readable string.
    
    Args:
        instructions (list): List of TAC instructions
        
    Returns:
        str: A readable string representation of the TAC instructions
    """
    formatted = []
    
    # Add a header
    formatted.append("Three-Address Code (TAC):")
    formatted.append("-" * 30)
    
    # Format each instruction with line numbers
    for i, instr in enumerate(instructions):
        formatted.append(f"{i}: {format_instruction(instr)}")
    
    return "\n".join(formatted)

def print_tac(instructions):
    """
    Print TAC instructions in a readable format.
    
    Args:
        instructions (list): List of TAC instructions
    """
    print(format_tac(instructions))

if __name__ == "__main__":
    # Example TAC instructions for testing
    example_tac = [
        {'type': 'assign', 'lhs': 'a', 'rhs': '5'},
        {'type': 'assign', 'lhs': 'b', 'rhs': '7'},
        {'type': 'binop', 'lhs': 't0', 'op': '+', 'arg1': 'a', 'arg2': 'b'},
        {'type': 'assign', 'lhs': 'c', 'rhs': 't0'},
    ]
    
    # Print the example
    print_tac(example_tac)