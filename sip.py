import argparse
import os
import sys
from llvmlite import binding
from llvmlite import ir
from parser.parser.siVisitor import siVisitor
from parser.parser.siParser import siParser
from antlr4 import *
from parser.parser.siLexer import siLexer
from parser.parser.siParser import siParser


class LLVMCodeGenVisitor(siVisitor):
    def __init__(self):
        self.module = ir.Module(name=__file__)
        self.builder = None
        self.func = None

        # # Initialize LLVM target
        # binding.initialize()
        # binding.initialize_native_target()
        # binding.initialize_native_asmprinter()

        # # Setting Target triple and Data layout
        # self.module.triple = binding.get_default_triple()
        # target = binding.Target.from_triple(self.module.triple)
        # target_machine = target.create_target_machine()
        # self.module.data_layout = target_machine.target_data

    def generate_ir(self, tree):
        func_type = ir.FunctionType(ir.IntType(32), ())
        self.func = ir.Function(self.module, func_type, name="main")
        block = self.func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        result = self.visit(tree)
        self.builder.ret(result)

    def visitProg(self, ctx: siParser.ProgContext):
        return self.visit(ctx.expr(0))

    def visitExpr(self, ctx: siParser.ExprContext):
        if ctx.INT():
            return ir.Constant(ir.IntType(32), int(ctx.INT().getText()))

        elif ctx.op:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            if ctx.op.text == '+':
                return self.builder.add(left, right, name="addtmp")
            elif ctx.op.text == '-':
                return self.builder.sub(left, right, name="subtmp")
            elif ctx.op.text == '*':
                return self.builder.mul(left, right, name="multmp")
            elif ctx.op.text == '/':
                return self.builder.sdiv(left, right, name="divtmp")

        elif ctx.expr(0):
            return self.visit(ctx.expr(0))

        return ir.Constant(ir.IntType(32), 0)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_file', type=str,
                        help='Input file containing arithmetic expressions')
    parser.add_argument('-o', '--output', type=str,
                        default='output.ll', help='Output file for LLVM IR')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output

    with open(input_file, 'r') as file:
        input_stream = InputStream(file.read())

    lexer = siLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = siParser(stream)
    tree = parser.prog()

    codegen = LLVMCodeGenVisitor()
    codegen.generate_ir(tree)

    with open(output_file, 'w') as file:
        file.write(str(codegen.module))

    print(output_file)


if __name__ == '__main__':
    main()
