#!/usr/bin/env python3

#    Copyright (C) 2020 Captain Foxtrot.

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Constants
MEMORYSIZE:int = 10000
STACKSIZE:int = 10000

# Initialize code area and code pointer
code:str = ""
codePtr:int = 0

# Initialize memory
memory:bytearray = bytearray(MEMORYSIZE)
memoryPtr:int = 0

# Initialize stack
stack:bytearray = bytearray(STACKSIZE)

# Execute a single instruction (character)
def exec(char: str):

    global memory, memoryPtr, MEMORYSIZE, stack

    if char == "i":
        # Increment
        try: memory[memoryPtr] += 1
        # Integer overflow
        except ValueError: memory[memoryPtr] = 0

    elif char == "d":
        # Decrement
        try: memory[memoryPtr] -= 1
        # Integer underflow
        except ValueError: memory[memoryPtr] = 256

    elif char == "l":
        # Decrement pointer
        if memoryPtr: memoryPtr -= 1
        # About to underflow?
        else: memoryPtr = MEMORYSIZE - 1

    elif char == "r":
        # Increment pointer
        if memoryPtr == 256: memoryPtr = 0
        # About to overflow?
        else: memoryPtr += 1

    elif char == "n":
        # Append value of pointer to stack
        stack.append(memory[memoryPtr])

    elif char == "f":
        # Overwrite value of pointer with top item on stack
        memory[memoryPtr] = stack[-1]
        # Drop an item from the stack
        del stack[-1]

    elif char == "s":
        # Check if the value of the pointer is greater than zero
        if memory[memoryPtr] != 0:
            # Jump forward x number of spaces where x is the value on the top of the stack
            codePtr += stack[-1]

            assert codePtr < len(code)
        # Drop an item from the stack
        del stack[-1]

    elif char == "b":
        # Check if the value of the pointer is greater than zero
        if memory[memoryPtr] != 0:
            # Jump forward x number of spaces where x is the value on the top of the stack
            codePtr -= stack[-1]

            assert codePtr >= 0
        # Drop an item from the stack
        del stack[-1]

    elif char == "o":
        # Print the value of the pointer as an ASCII character, without a newline
        print(chr(memory[memoryPtr]), end = "")

    # Any characters that are not commands will throw an error.
    else:
        raise Exception("Unrecognized command: " + char)

# Pass a string of NoComment code into this function to run it.
def exec_str(_code: str):

    global codePtr

    while codePtr < len(_code):
        exec(_code[codePtr])
        codePtr += 1
        
# This part will not be run if this script is being run through an import.
if __name__ == "__main__":

    import sys

    # Read the contents of the file into `code`
    try:
        FILENAME:str = sys.argv[1]
        with open(FILENAME, "r") as codeFile:
            code = codeFile.read()

    # User did not enter a file to run, enter REPL
    except IndexError:
        print("Enter the name of a file to run.")

    # File does not exist
    except FileNotFoundError:
        print(f"File {FILENAME} does not exist.")
        sys.exit(1)

    # Execute the code
    exec_str(code)
