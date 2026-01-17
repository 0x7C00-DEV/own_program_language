from typing import override
import time
import Lexer
import Parser
import Interpreter
from Interpreter import Context

def file_test():
    f = open('test.opl', 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    lexer = Lexer.Lexer(data)
    parser = Parser.Parser(lexer.tokens)
    context = Context({}, None)
    ip = Interpreter.Interpreter(parser.asts, context)

def shell():
    text = ''
    while True:
        data = input('shell > ')
        if data == 'RUN':
            lexer = Lexer.Lexer(data)
            parser = Parser.Parser(lexer.tokens)
            context = Context({}, None)
            begin = time.time()
            ip = Interpreter.Interpreter(parser.asts, context)
            end = time.time()
            print(f'Program[TIME: ({end - begin}), RES: {ip.res}]')
        else:
            text += data 

if __name__ == '__main__':
    file_test()