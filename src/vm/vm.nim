#[
Nim VM, Virtual machine for compiling and interepreting the hanual bytecode. It is speedy as nim is complied to C.
!! DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!
because I definitely do.

        # Notes on bytecode

     

        # File extension (Not related to chernobal)
        .chnl

        # Docs links
        https://nim-lang.org/docs/manual.html#exception-handling
        https://nim-lang.org/docs/manual.html#statements-and-expressions-while-statement
        https://nim-lang.org/docs/os.html
        https://nim-lang.org/docs/tut2.html#exceptions-raise-statement
        https://stackoverflow.com/questions/34427858/reading-bytes-from-many-files-performance
]#

# Imports
import os
import std/os

# Parse file into various parts (Instruction, const, etc. pools)
var
    f: File
    end: False

if open(f, "main.chnl"):
    while end != True:
        for instructions in f:
            ...
else:
    raise "The main file does not exist, touch the main.chnl file if you are on unix based systems"
