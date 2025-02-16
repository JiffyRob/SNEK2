from SNEK2.scan import Scanner
from SNEK2.parse import Parser
from SNEK2.ast_printer import AstPrinter
from SNEK2.interpret import Interpreter

def main():
    with open("exp.snek") as f:
        source = f.read()
    
    scanner = Scanner(source)
    tokens = scanner.scan()
    parser = Parser(tokens)
    expression = list(parser.parse())
    interpreter = Interpreter()
    interpreter.interpret(expression)


if __name__ == "__main__":
    main()