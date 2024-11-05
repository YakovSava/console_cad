from sys import argv

from plugins.cad import CADConsole
from plugins.lexer import Lexer

cad_console = CADConsole()
if len(argv) > 1:
    lexer = Lexer(argv[1])
    for command in lexer.compile():
        cad_console.execute_command(command)
    print("File processed!")
else:
    print("Enter CAD commands (type 'exit' to finish):")
    while True:
        command = input(">>> ")
        if command.lower() == 'exit':
            break
        cad_console.execute_command(command)

cad_console.save()