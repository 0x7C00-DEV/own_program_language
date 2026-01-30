from Lexer import *


class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

class ReturnNode:
    def __init__(self, value):
        self.value = value 

    def __repr__(self):
        return f'Return({self.value})'

class NumberNode:
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f'{self.num}'

class StringNode:
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return f'String("{self.string}")'

class BitNotNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'BitNot({self.value})'

class BoolNode:
    def __init__(self, bol):
        self.bol = bol

    def __repr__(self):
        return f'Bool<{self.bol}>'

class MemberAccessNode:
    def __init__(self, parent, field):
        self.parent = parent
        self.fiele = field

    def __repr__(self):
        return f'({self.parent} -> {self.fiele})'

class CallNode:
    def __init__(self, name, param = []):
        self.name = name
        self.param = param

    def __repr__(self):
        return f'Call({self.name}, {self.param})'

class IfNode:
    def __init__(self, condition, true, else_):
        self.condition = condition
        self.if_true = true
        self._else = else_

    def __repr__(self):
        return f'If({self.condition})[{self.if_true}][{self._else}]'

class FunctionNode:
    def __init__(self, name, params, body):
        self.name = name
        self.param = params
        self.body = body

    def __repr__(self):
        return f'Function[{self.name}, {self.param}, {self.body}]'

class ArrayNode:
    def __init__(self, elements = []):
        self.elements = elements

    def __repr__(self):
        return f'Arr{self.elements}'

class VarDefineNode:
    def __init__(self, name, init_value = None):
        self.name = name
        self.init_value = init_value

    def __repr__(self):
        return f'Def[{self.name}, {self.init_value}]'

class BlockNode:
    def __init__(self, bl = []):
        self.codes = bl

    def __repr__(self):
        return f'Block[{self.codes}]'
    
class ElementGetNode:
    def __init__(self, name, pos):
        self.name = name 
        self.pos  = pos 

    def __repr__(self):
        return f'ElementGet({self.name}, {self.pos})'
    
class ClassNode:
    def __init__(self, name, fields: dict[str, any]):
        self.fields = fields
        self.name   = name

    def __repr__(self):
        return f'Class[{self.fields}]'
    
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'While[{self.condition}, {self.body}]'
    
class ForLoopNode:
    def __init__(self, init, is_loop, change, body):
        self.init = init
        self.is_loop = is_loop
        self.change = change 
        self.body = body 

    def __repr__(self):
        return f'ForLoopNode[{self.init}, {self.is_loop}, {self.change}]({self.body})'
    
class FunctionDefineNode:
    def __init__(self, name, params, body):
        self.name = name 
        self.params = params
        self.body = body 

    def __repr__(self):
        return f'Function[{self.name}, {self.params}, {self.body}]'


SEL_PRE = 'PRE' # 前缀
SEL_SUF = 'SUF' # 后缀
    
class IncNode:
    def __init__(self, id, kind = SEL_PRE):
        self.id = id
        self.kind = kind

    def __repr__(self):
        return f'Inc({self.id})'
    
class ContinueNode:
    def __init__(self):
        pass

    def __repr__(self):
        return f'Continue'
    
class NoneNode:
    def __init__(self):
        pass
    
    def __repr__(self):
        return 'null'

class BreakNode:
    def __init__(self): pass

    def __repr__(self): return 'Break'


class NewNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'New[{self.name}, {self.args}]'

class DecNode:
    def __init__(self, id, kind = SEL_PRE):
        self.id = id
        self.kind = kind

    def __repr__(self):
        return f'Dec({self.id})'
    
class AssignNode:
    def __init__(self, id, value):
        self.id = id 
        self.value = value 

    def __repr__(self):
        return f'Assign({self.id}, {self.value})'

class Parser:
    def __init__(self, tokens: list[Token] = []):
        self.tokens = tokens
        self.pos = -1
        self.current: Token = None
        self.asts = []
        self.advance()
        self.make_all()

    def make_all(self):
        while self.current is not None:
            if self.current.data == 'for':
                self.asts.append(self.make_for_loop())
            elif self.current.data == 'while':
                self.asts.append(self.make_while_loop())
            elif self.current.data == 'func':
                self.asts.append(self.make_function_define())
            elif self.current.data == 'class':
                self.asts.append(self.make_class_define())
            elif self.current.data == 'new':
                self.asts.append(self.make_new_node())
            elif self.current.data == 'if':
                self.asts.append(self.make_if())
            elif self.current.data == 'func':
                self.asts.append(self.make_function_define())
            elif self.current.data == 'for':
                self.asts.append(self.make_for_loop())
            elif self.current.data == 'while':
                self.asts.append(self.make_while_loop())
            elif self.current.data == 'let':
                self.asts.append(self.make_var_define())
                self.expect_value(';')
            else:
                tmp = self.make_expression()
                if self.match_value('='):
                    tmp = self._make_assign_node(tmp)
                if self.match_value('++'):
                    self.advance()
                    tmp = IncNode(tmp, SEL_SUF)
                if self.match_value('--'):
                    self.advance()
                    tmp = DecNode(tmp, SEL_SUF)
                self.asts.append(tmp)
                self.expect_value(';')

    def make_null_node(self):
        self.advance()
        return NoneNode()

    def make_new_node(self):
        self.expect_value('new')
        name = self.current.data
        args = {}
        self.advance()
        self.expect_value('{')
        while self.current is not None and not self.match_value('}'):
            vname = self.current.data
            self.advance()
            self.expect_value(':')
            val = self.make_value()
            args[vname] = val
            if self.match_value(','): self.advance()
            if self.match_value('}'): break
        self.expect_value('}')
        return NewNode(name, args)

    def _make_assign_node(self, id):
        self.expect_value('=')
        val = self.make_expression()
        return AssignNode(id, val)

    def make_assign_node(self):
        if self.match_value('++'):
            self.advance()
            return IncNode(self.make_member_access(), SEL_PRE)
        if self.match_value('--'):
            self.advance()
            return DecNode(self.make_member_access(), SEL_PRE)
        tmp = self.make_member_access()
        op  = self.current.data
        self.advance()
        if op == '++':
            return IncNode(tmp, SEL_SUF)
        if op == '--':
            return DecNode(tmp, SEL_SUF)
        if op == '=':
            val = self.make_expression()
            return AssignNode(tmp, val)
        raise 'UNKNOWN OPERATOR' + op  
    
    def make_class_define(self):
        self.expect_value('class')
        name = self.current.data
        tmp = {}
        self.advance()
        self.expect_value('{')
        while self.current is not None and not self.match_value('}'):
            fin = self.current.data
            self.advance()
            self.expect_value(':')
            typ = self.current.data
            self.advance()
            tmp[fin] = typ
            if self.match_value('}'): break
            self.expect_value(',')
        self.expect_value('}')
        return ClassNode(name, tmp)

    def make_function_define(self):
        self.expect_value('func')
        name = self.current.data
        args = []
        self.advance()
        self.expect_value('(') 
        while self.current != None and not self.match_value(')'):
            args.append(self.make_var_define())
            if self.current.data == ')': break
            self.expect_value(',')
        self.expect_value(')')
        body = self.make_block()
        return FunctionDefineNode(name, args, body) 

    def make_for_loop(self):
        self.expect_value('for')
        self.expect_value('(')
        init = self.make_var_define()
        self.expect_value(';')
        is_loop = self.make_expression()
        self.expect_value(';')
        change = self.make_assign_node()
        self.expect_value(')')
        body = self.make_block()
        return ForLoopNode(init, is_loop, change, body)

    def make_while_loop(self):
        self.expect_value('while')
        condition = self.make_value()
        block = self.make_block()
        return WhileNode(condition, block)

    def advance(self):
        self.pos += 1
        self.current = None
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def make_if(self):
        self.expect_value('if')
        condition = self.make_value()
        body = self.make_block()
        el = None
        if self.match_value('else'):
            self.advance()
            el = self.make_block()
        return IfNode(condition, body, el)

    def make_block(self):
        self.expect_value('{')
        b = []
        while self.current is not None:
            if self.match_value('for'):
                b.append(self.make_for_loop())
            elif self.match_value('return'):
                b.append(self.make_return())
                self.expect_value(';')
            elif self.match_value('break'):
                b.append(BreakNode())
                self.advance()
                self.expect_value(';')
            elif self.match_value('continue'):
                b.append(ContinueNode())
                self.advance()
                self.expect_value(';')
            elif self.match_value('new'):
                b.append(self.make_new_node())
                self.expect_value(';')
            elif self.match_value('while'):
                b.append(self.make_while_loop())
            elif self.match_value('let'):
                b.append(self.make_var_define())
                self.expect_value(';')
            elif self.match_value('if'):
                b.append(self.make_if())
            elif self.match_value('}'):
                break
            else:
                tmp = self.make_expression()
                if self.match_value('='):
                    tmp = self._make_assign_node(tmp)
                if self.match_value('++'):
                    self.advance()
                    tmp = IncNode(tmp, SEL_SUF)
                if self.match_value('--'):
                    self.advance()
                    tmp = DecNode(tmp, SEL_SUF)
                b.append(tmp)
                self.expect_value(';')

        self.expect_value('}')
        return BlockNode(b)

    def make_bin_op(self, left_process, opers, right_process = None):
        left = left_process()
        if right_process == None:
            right_process = left_process
        while self.current != None and self.current.data in opers:
            op = self.current.data
            self.advance()
            right = right_process()
            left = BinOpNode(op, left, right)
        return left

    def match_value(self, value):
        if self.current is None:
            return False
        return self.current.data == value

    def match_type(self, type_):
        if self.current is None:
            return False
        return self.current.type == type_

    def make_member_access(self):
        parent = self.current.data
        self.advance()
        while self.current is not None and self.current.data == '.':
            self.advance()
            field = self.current.data
            self.advance()
            parent = MemberAccessNode(parent, field)
        return parent

    def make_expression(self):
        return self.make_bin_op(self.make_expression_5, ('or'))

    def make_expression_5(self):
        return self.make_bin_op(self.make_expression_4, ('and'))

    def make_expression_4(self):
        return self.make_bin_op(self.make_expression_3, ('>', '<', '>=', '<=', '==', '!='))

    def make_expression_3(self):
        return self.make_bin_op(self.make_expression_2, ('+', '-', '>>', '<<'))

    def make_expression_2(self):
        return self.make_bin_op(self.make_expression_1, ('/', '*', '%'))

    def make_expression_1(self):
        return self.make_bin_op(self.make_value, ('**'))

    def expect_value(self, value):
        if not self.match_value(value):
            print(f'SymtaxError: want "{value}", got "{self.current.data}", at {self.current.pos_begin}')
            exit(-1)
        self.advance()

    def make_call_(self, name):
        if not self.match_value('('): return name
        params = []
        self.advance()
        while self.current is not None and not self.match_value(')'):
            params.append(self.make_expression())
            if self.match_value(')'): break
            self.expect_value(',')
        self.expect_value(')')
        return CallNode(name, params)
    
    def make_return(self):
        self.expect_value('return')
        return ReturnNode(self.make_expression())

    def make_element_get(self, name):
        self.expect_value('[')
        pos = self.make_expression()
        self.expect_value(']')
        tmp = ElementGetNode(name, pos)
        while self.current is not None and self.match_value('['):
            self.advance()
            ptemp = self.make_expression()
            self.expect_value(']')
            tmp = ElementGetNode(tmp, ptemp)
        return tmp 

    def make_call(self, name):
        tmp = self.make_call_(name)
        if self.match_value('['): tmp = self.make_element_get(tmp)
        while self.current is not None and self.match_value('('):
            tmp = self.make_call_(tmp)
            if self.match_value('['): tmp = self.make_element_get(tmp)
        return tmp

    def make_var_define(self):
        self.expect_value('let')
        name = self.current.data
        self.advance()
        init_value = None
        if self.match_value('='):
            self.advance()
            init_value = self.make_expression()
        return VarDefineNode(name, init_value)

    def make_value(self):
        if self.match_value('new'):
            return self.make_new_node()
        if self.match_value('null'):
            return self.make_null_node()
        if self.match_value('++'):
            self.advance()
            return IncNode(self.make_expression(), SEL_PRE)
        if self.match_value('--'):
            self.advance()
            return DecNode(self.make_expression(), SEL_PRE)
        if self.match_type(TT_NUM):
            tmp = NumberNode(self.current.data)
            self.advance()
            return tmp
        if self.match_type(TT_BOOL):
            tmp = BoolNode(self.current.data)
            self.advance()
            return tmp
        if self.match_type(TT_ID):
            tmp = self.make_call(self.make_member_access())
            if self.match_value('++'):
                self.advance()
                tmp = IncNode(tmp, SEL_SUF)
            if self.match_value('--'):
                self.advance()
                tmp = DecNode(tmp, SEL_SUF)
            return tmp
        if self.match_value('['):
            self.advance()
            elements = []
            while self.current is not None and not self.match_value(']'):
                elements.append(self.make_expression())
                if self.match_value(']'): break
                self.expect_value(',')
            self.expect_value(']')
            return ArrayNode(elements)
        if self.match_type(TT_STR):
            tmp = StringNode(self.current.data)
            self.advance()
            return tmp
        if self.match_value('-'):
            self.advance()
            return BinOpNode('*', NumberNode('-1.0'), self.make_expression())
        if self.match_value('~'):
            self.advance()
            return BitNotNode(self.make_expression())
        if self.match_value('('):
            self.advance()
            tmp = self.make_expression()
            self.expect_value(')')
            return tmp
        else:
            if self.current is None:
                print("MeetEof")
                exit(-1)
            print(f'UnknownSyntaxError: "{self.current.data}", at {self.current.pos_begin}')
            exit(-1)