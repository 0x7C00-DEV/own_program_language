class Position:
    def __init__(self, lin, col):
        self.lin = lin
        self.col = col

    def __repr__(self):
        return f'POS({self.lin}, {self.col})'

class Token:
    def __init__(self, tok_data, tok_kind, pos_begin: Position, pos_end: Position):
        self.data = tok_data
        self.type = tok_kind
        self.pos_begin = pos_begin
        self.pos_end   = pos_end

    def __repr__(self):
        return f'("{self.data}", {self.type})'

TT_NUM = 'NUMBER'
TT_STR = 'STR'
TT_ID  = 'ID'
TT_KEY = 'KEY'
TT_OP  = 'OP'
TT_BOOL = 'BOOL'

keys = ['if', 'else', 'for', 'while', 'func', 'return', 'continue', 'break', 'let', 'class', 'new']

class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self.pos  = -1
        self.current = None
        self.tokens = []
        self.uSymbol = ['==', '!=', '>=', '<=', '**', '>>', '<<', '++', '--', '>>=', '<<=', '+=', '-=', '/=', '*=']
        self.lin = 1
        self.col = 1
        self.advance()
        self.make_tokens()

    def advance(self, len_ = 1) -> None:
        self.pos += len_
        self.current = None
        if self.pos < len(self.expr):
            self.current = self.expr[self.pos]
            if self.current != '\n':
                self.col += 1
            elif self.current == '\n':
                self.col = 1
                self.lin += 1

    def forward_comp(self, ex: str) -> bool:
        if self.pos + len(ex) >= len(self.expr):
            return False
        for i in range(len(ex)):
            if self.expr[self.pos + i] != ex[i]:
                return False
        return True

    def make_pos(self) -> Position:
        return Position(self.lin, self.col)

    def make_digit(self):
        res = ''
        pos_begin = self.make_pos()
        while self.current is not None and ('0' <= self.current <= '9' or self.current == '.'):
            res += self.current
            self.advance()
        pos_end = self.make_pos()
        return Token(res, TT_NUM, pos_begin, pos_end)

    def make_string(self):
        eof = self.current
        self.advance()
        ss = ''
        begin = self.make_pos()
        while self.current is not None and self.current != eof:
            if self.current != '\\':
                ss += self.current
                self.advance()
            else:
                self.advance()
                nt = self.current
                self.advance()
                if nt == 'n': ss += '\n'
                elif nt == 'r': ss += '\r'
                elif nt == 't': ss += '\t'
                elif nt == 'a': ss += '\a'
                elif nt == 'b': ss += '\b'
                elif nt == 'f': ss += '\f'
                else: ss += nt 
        end = self.make_pos()
        if self.current != eof:
            print(f'SyntaxError: want a "{eof}", but got "{self.current}", at {end}')
            exit(-1)
        self.advance()
        return Token(ss, TT_STR, begin, end)

    def make_id(self):
        id_str = ''
        kind = TT_ID
        begin = self.make_pos()
        while self.current is not None and ('a' <= self.current <= 'z' or 'A' <= self.current <= 'Z' or self.current == '_'):
            id_str += self.current
            self.advance()
        end = self.make_pos()
        if id_str in keys:
            kind = TT_KEY
        elif id_str == 'false' or id_str == 'true':
            kind = TT_BOOL
        return Token(id_str, kind, begin, end)

    def make_tokens(self):
        while self.current is not None:
            if '0' <= self.current <= '9':
                self.tokens.append(self.make_digit())
            elif self.current == '#':
                while self.current is not None and self.current != '\n':
                    self.advance()
            elif 'a' <= self.current <= 'z' or 'A' <= self.current <= 'Z':
                self.tokens.append(self.make_id())
            elif self.current == '\'' or self.current == '"':
                self.tokens.append(self.make_string())
            elif not self.current.isspace():
                is_find = False
                for i in self.uSymbol:
                    if self.forward_comp(i):
                        is_find = True
                        begin = self.make_pos()
                        self.advance(len(i))
                        end = self.make_pos()
                        self.tokens.append(Token(i, TT_OP, begin, end))
                        break
                if is_find:
                    continue
                oper = self.current
                begin = self.make_pos()
                self.advance()
                end = self.make_pos()
                self.tokens.append(Token(oper, TT_OP, begin, end))
            else:
                self.advance()