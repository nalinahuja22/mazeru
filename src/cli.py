# Developed by Nalin Ahuja, nalinahuja22

import os

# End Imports------------------------------------------------------------------------------------------------------------------------------------------------------------

# Newline
NL = "\n"

# Carriage Return
CR = "\r"

# Cursor Up ANSI Sequence
UP = "\033[A"

# Clear Line ANSI Sequence
CL = "\033[2K"

# End String Constants---------------------------------------------------------------------------------------------------------------------------------------------------

def nl(num):
    # Return New Line Sequence
    return ((NL) * num)

def cl(num):
    # Print Clear Line Sequence
    print((UP + CL + CR) * num, end = "")

def size():
    # Return Terminal Size
    return (os.get_terminal_size())

def prompt(msg):
    # Create Input Prompt
    result = input(msg)

    # Return Formatted Result
    return (result.strip())

# End Interface Functions------------------------------------------------------------------------------------------------------------------------------------------------
