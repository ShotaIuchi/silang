import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from parser.parser.siLexer import siLexer
from parser.parser.siParser import siParser


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = siLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = siParser(stream)
    tree = parser.expr()
    print(Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main(sys.argv)
