FILENAME = "assembly.txt"
PROGRAM_NAME = "TEST"

# TODO: manage the start of the program, check opcodes

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
    for line in lines:
        if len(line.split(" ")) == 3:
            definitions.append(line)
        else:
            instructions.append(line)
    return instructions, definitions

# Format a string to a given length by adding 0 at the beginning
def format_bytes(string, length):
    return "0" * (length - len(string)) + string

# Returns the symbol table which associate each symbol with its address
def first_phase():
    symbol_table = {}
    starting_address = len(definitions) * 3
    for i in range(len(definitions)):
        symbol = definitions[i].split(" ")[0]
        # store the address of the symbol in the symbol table in hexadecimal
        if symbol in symbol_table:
            print("Error: symbol already defined, line " + str(i))
            return {}
        symbol_table[symbol] = hex(starting_address + i * 3 - 3)

    return symbol_table

# Use the symbol table and the instructions to generate the machine code in the form of a list of 6 bytes arrays
def second_phase(symbol_table):
    machine_code = []
    for line in instructions:
        # Get the opcode
        opcode = line.split(" ")[0]
        # Get the operand and remove the \n if it exists
        operand = line.split(" ")[1].replace("\n", "")
        # Get the address of the operand
        if operand in symbol_table.keys():
            address = symbol_table[operand]
        else:
            print(type(operand))
            print(symbol_table[operand])
            print("Error: symbol not defined, line " + str(instructions.index(line)))
            return
        # Create a 6 bytes array and store the machine code
        opcode_value = opcodes[opcode]
        code = format_bytes(str(hex(opcode_value))[2:].upper(), 2) + format_bytes(str(address)[2:].upper(), 4)
        machine_code.append(code)

    for i in definitions:
        if ("HALT" in i):
            machine_code.append("3C" + format_bytes(str(symbol_table[i.split(" ")[0]])[2:].upper(), 4))
        elif ("RESW" in i):
            continue
        else:
            machine_code.append("0" * 2 + format_bytes(str(hex(int(i.split(" ")[2]))[2:].upper()), 4))

    return machine_code

#Write the machine code in the .obj file
def third_phase(machine_code):
    # Write the machine code in a file
    outputLines = []
    outputLines.append(
        "H" + PROGRAM_NAME + " " * (6 - len(PROGRAM_NAME)) + "000000" + hex(len(machine_code) * 3)[2:].upper())
    outputLines.append("T" + "000000" + hex(len(machine_code) * 3)[2:].upper() + "".join(machine_code))
    outputLines.append("E" + "000000")
    with open("output.obj", "w") as f:
        f.write("\r".join(outputLines))


def main():
    # Store the file in a list
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
    instructions, definitions = separate_lines(lines)
    # print(definitions)
    symbol_table = first_phase()
    machine_code = second_phase(symbol_table)
    # print(symbol_table)
    # print(machine_code)
    third_phase(machine_code)


main()
