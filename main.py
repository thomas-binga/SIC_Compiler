from LineParser import LineParser

FILENAME = ""
PROGRAM_NAME = ""

# Opcode table
opcodes = {
    'ADD': 0x18,
    'AND': 0x40,
    'COMP': 0x28,
    'DIV': 0x24,
    'J': 0x3C,
    'JEQ': 0x30,
    'JGT': 0x34,
    'JLT': 0x38,
    'JSUB': 0x48,
    'LDA': 0x00,
    'LDCH': 0x50,
    'LDL': 0x08,
    'LDX': 0x04,
    'MUL': 0x20,
    'OR': 0x44,
    'RD': 0xD8,
    'RSUB': 0x4C,
    'STA': 0x0C,
    'STCH': 0x54,
    'STL': 0x14,
    'STX': 0x10,
    'SUB': 0x1C,
    'TD': 0xE0,
    'TIX': 0x2C,
    'WD': 0xDC
}


# Separate lines into instructions and definitions
def separate_lines(lines):
    instructions = []
    definitions = []
    started = False
    for line in lines:
        if len(line) < 5:
            continue
        if not started and line.split()[1] == "START":
            global PROGRAM_NAME
            PROGRAM_NAME = str(line.split()[0])
            started = True
        elif len(line.split()) == 3:
            definitions.append(LineParser(line))
        else:
            instructions.append(LineParser(line))

    return instructions, definitions


# Format a string to a given length by adding 0 at the beginning
def format_bytes(string, length):
    return "0" * (length - len(string)) + string


# Returns the symbol table which associate each symbol with its address
def first_phase(definitions):
    symbol_table = {}
    starting_address = len(definitions) * 3
    for i in range(len(definitions)):
        symbol = definitions[i].get_first_arg()
        # store the address of the symbol in the symbol table in hexadecimal
        if symbol in symbol_table:
            print("Error: symbol already defined, line " + str(i))
            return {}
        symbol_table[symbol] = hex(starting_address + i * 3 - 3)
    return symbol_table


# Use the symbol table and the instructions to generate the machine code in the form of a list of 6 bytes arrays
def second_phase(symbol_table, instructions, definitions):
    machine_code = []
    if symbol_table == {}:  # Error in the first phase
        return []
    for line in instructions:
        # Get the opcode
        opcode = line.get_first_arg()
        # Get the operand and remove the \n if it exists
        operand = line.get_second_arg()
        # Get the address of the operand
        if operand in symbol_table.keys():
            address = symbol_table[operand]
        else:
            # print(symbol_table[operand])
            print("Error: symbol not defined, line " + str(instructions.index(line)))
            return []
        # Create a 6 bytes array and store the machine code
        opcode_value = opcodes[opcode]
        code = format_bytes(str(hex(opcode_value))[2:].upper(), 2) + format_bytes(str(address)[2:].upper(), 4)
        machine_code.append(code)

    for line in definitions:
        if "HALT" in line:
            machine_code.append("3C" + format_bytes(str(symbol_table[line.get_first_arg()])[2:].upper(), 4))
        elif "RESW" in line:
            continue
        else:
            machine_code.append("0" * 2 + format_bytes(str(hex(int(line.get_third_arg()))[2:].upper()), 4))

    return machine_code


# Write the machine code in the .obj file
def third_phase(machine_code):
    if not machine_code:  # Error in the second phase
        return
    # Write the machine code in a file
    output_lines = [
        "H" + PROGRAM_NAME + " " * (6 - len(PROGRAM_NAME)) + "0000000000" + hex(len(machine_code) * 3 + 3)[2:].upper(),
        "T000000" + hex(len(machine_code) * 3)[2:].upper() + "".join(machine_code),
        "E000000"]
    with open(FILENAME + ".obj", "w") as f:
        f.write("\r".join(output_lines))


def main():
    # Ask the user for the file name
    global FILENAME
    FILENAME = input("Enter the file name without the .asm extension: ")

    # Open the file
    # Store the file in a list
    with open(FILENAME + '.asm', 'r') as f:
        lines = f.readlines()
    instructions, definitions = separate_lines(lines)
    # print(definitions)
    symbol_table = first_phase(definitions)
    machine_code = second_phase(symbol_table, instructions, definitions)
    # print(symbol_table)
    # print(machine_code)
    third_phase(machine_code)


if __name__ == "__main__":
    main()
