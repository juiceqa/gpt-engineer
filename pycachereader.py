import dis
# Specify the path to the .pyc file
pyc_file = "__pycache__/chat_to_files.cpython-311.pyc"

# Load and disassemble the bytecode
with open(pyc_file, "rb") as file:
    bytecode = file.read()

dis.dis(bytecode)
