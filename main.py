from plugins.cad import CADConsole

cad_console = CADConsole()

print("Enter CAD commands (type 'exit' to finish):")
while True:
    command = input(">>> ")
    if command.lower() == 'exit':
        break
    cad_console.execute_command(command)

cad_console.save()