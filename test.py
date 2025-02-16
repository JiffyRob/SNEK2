from SNEK2.scan import Scanner
from SNEK2.parse import Parser
from SNEK2.ast_printer import AstPrinter

def main():
    with open("exp.snek") as f:
        source = f.read()
    
    scanner = Scanner(source)
    tokens = scanner.scan()
    parser = Parser(tokens)
    expression = parser.parse()
    printer = AstPrinter()
    print(printer.print(expression))


if __name__ == "__main__":
    main()