from yacc import build_parser
import sys


parser = build_parser()

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        assembly = parser.parse(file.read())
        if assembly:
            
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'w') as output:
                    output.write(assembly)
                    print(f"{sys.argv[1]} compiled successfully!\nCheck the output in {sys.argv[2]}.")
            else:
                print(f"{sys.argv[1]} compiled successfully!")
        else:
            print("Empty!")
else:
    line = input(">")
    while line!="\n":
        print(parser.parse(line))
        line = input(">")
