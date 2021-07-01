from pyparsing import Word, hexnums, WordEnd, Optional, alphas, alphanums
import os
import pandas as pd

def extration_code(file_name):
    hex_integer = Word(hexnums) + WordEnd()
    line = (
        ".text:"
        + hex_integer
        + Optional((hex_integer * (1,))("instructions") + Word(alphas, alphanums)("opcode"))
    )
    opcodes=[]
    with open(file_name) as source:
        for source_line in source:
            source_line = source_line.strip()
            if source_line[:5] == ".text":
                result = line.parseString(source_line)
                if "opcode" in result:
                    opcodes.append(result.opcode)
            elif source_line[:5] != ".text":
                pass
            else:
                break
    extracted_seq=" ".join(opcodes)
    data = {'clean_seq':extracted_seq}
    os.remove(file_name)
    return data
#extraction_code(file_data)
