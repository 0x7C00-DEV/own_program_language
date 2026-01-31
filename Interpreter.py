from Lexer import *
from Parser import *

class NameNotFound: pass 

class Context:
    def __init__(self, table, parent = None, display_name = '<Program>'):
        self.parent = parent
        self.table: dict[str, any] = table
        self.display_name = display_name

    def __repr__(self):
        return f'Context ({self.parent}, {self.table}, {self.display_name})'

    def add(self, name, value = None):
        self.table[name] = value

    def set(self, name, value = None):
        if type(self.table.get(name, NameNotFound())).__name__ == 'NameNotFound' and self.parent is not None:
            self.parent.set(name, value)
            return 
        if type(self.table.get(name, NameNotFound())).__name__ != 'NameNotFound':
            self.table[name] = value 
            return 
        raise NameError(f'Name "{name}" is not found')

    def get(self, name):
        tmp = self.table.get(name, None)
        if tmp != None: return tmp
        if self.parent != None: return self.parent.get(name)

class Value:
    def __init__(self):
        pass

    def operator_not_aupposed(self, op):
        raise SyntaxError(f'operator symbol "{op}" is not supposed')

    def __comp_big__(self, other):
        self.operator_not_aupposed('>')

    def __comp_less__(self, other):
        self.operator_not_aupposed('<')

    def __comp_eq__(self, other):
        self.operator_not_aupposed('==')

    def __comp_neq__(self, other):
        self.operator_not_aupposed('!=')

    def __comp_big_or_eq__(self, other):
        self.operator_not_aupposed('>=')

    def __comp_less_or_eq__(self, other):
        self.operator_not_aupposed('<=')

    def left_move(self, other):
        self.operator_not_aupposed('<<')

    def right_move(self, other):
        self.operator_not_aupposed('>>')

    def added_by(self, other):
        self.operator_not_aupposed('+')

    def subbed_by(self, other):
        self.operator_not_aupposed('-')

    def muled_by(self, other):
        self.operator_not_aupposed('*')

    def dived_by(self, other):
        self.operator_not_aupposed('/')

class Number(Value):
    def __init__(self, number):
        self.number = number
        if type(self.number).__name__ == 'str':
            if self.number[0] == '-':
                self.number = -float(self.number[1:])
            else:
                self.number = float(self.number)

    def copy(self):
        return Number(self.number)

    def __iset__(self, other):
        self.number = other.number

    def __modd__(self, other):
        return Number(self.number % other.number) 

    def __comp_big__(self, other):
        return Bool(self.number > other.number)

    def __comp_less__(self, other):
        return Bool(self.number < other.number)

    def __comp_eq__(self, other):
        return Bool(self.number == other.number)

    def __comp_neq__(self, other):
        return Bool(self.number != other.number)

    def __comp_big_or_eq__(self, other):
        return Bool(self.number >= other.number)

    def __comp_less_or_eq__(self, other):
        return Bool(self.number <= other.number)

    def __repr__(self):
        return f'VM_Number({self.number})'

    def left_move(self, other):
        return Number(int(self.number) << int(other.number))

    def right_move(self, other):
        return Number(int(self.number) >> int(other.number))

    def added_by(self, other):
        return Number(self.number + other.number)

    def subbed_by(self, other):
        return Number(self.number - other.number)

    def muled_by(self, other):
        return Number(self.number * other.number)

    def dived_by(self, other):
        return Number(self.number / other.number)

class String(Value):
    def __init__(self, string):
        self.string = string

    def copy(self):
        return String(self.string)

    def __repr__(self):
        return f'String("{self.string}")'

    def __iset__(self, value):
        self.string = value.string
    
    def __length__(self):
        return Number(len(self.string))

    def __get_element__(self, pos):
        return String(self.string[int(pos.number)])

    def muled_by(self, other):
        return String(self.string * int(other.number))

    def added_by(self, other):
        return String(self.string + other.string)

class Bool(Value):
    def __init__(self, bol):
        self.bol = bol

    def copy(self):
        return Bool(self.bol)

    def __iset__(self, value):
        self.bol = value.bol

    def __repr__(self):
        return f'<{self.bol}>'

    def __cond_and__(self, other):
        return Bool(self.bol and other.bol)

    def __cond_or__(self, other):
        return Bool(self.bol or other.bol)

class Function(Value):
    def __init__(self, name, param, body):
        self.param = param
        self.body = body 
        self.name = name 

    def __repr__(self):
        return f'Function[PARAM: {self.param}, BODY: {self.body}]'

class Array(Value):
    def __init__(self, elements):
        self.elements = elements

    def __iset__(self, value):
        self.elements = value

    def copy(self):
        return Array(self.elements)

    def __length__(self):
        return Number(len(self.elements))

    def __repr__(self):
        return f'Arr{self.elements}'

    def added_by(self, other):
        self.elements.append(other)
        return self
    
    def __set_elemeny__(self, pos, value):
        self.elements[int(pos.number)] = value 

    def __get_element__(self, pos):
        return self.elements[int(pos.number)]
    
class StructTemplate(Value):
    def __init__(self, name, fields):
        self.fields = fields
        self.name   = name 

    def __repr__(self):
        return f'TMP[{self.fields}]'
    
class Null(Value):
    def __init__(self):
        pass 

    def __repr__(self):
        return f'null'

class Struct(Value):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def __iset__(self, name, value):
        self.fields[name].__iset__(value)

    def __field_get__(self, name):
        return self.fields.get(name, NameNotFound())

    def __repr__(self):
        return f'Struct[{self.name}, {self.fields}]'
    
class ReturnSignal: pass

class ContinueSignal: pass 

class BreakSignal: pass

class Interpreter:
    def __init__(self, codes, context: Context):
        self.context = context
        self.codes = codes
        self.setup_build_in_functions()
        self.res = None 
        self.visit_all()

    def visit_all(self):
        for i in self.codes:
            self.visit(i)

    def setup_build_in_functions(self):
        self.context.add('len', self.i_len)
        self.context.add('print', self.i_print)
        self.context.add('input', self.i_input)
        self.context.add('new_array', self.i_new_arr)
        self.context.add('number', self.i_string_to_float)
        self.context.add('string', self.i_float_to_string)

    def i_float_to_string(self, args: list[Number]):
        return String(str(args[0].number))

    def i_string_to_float(self, args: list[String]):
        return Number(float(args[0].string))

    def i_new_arr(self, length: list[any]):
        a = []
        for i in range(int(length[0].number)):
            a.append(Number(0.0))
        return Array(a)

    def i_input(self, name: list[any]):
        tmp = input(name[0].string)
        return String(tmp)

    def i_len(self, name):
        return name[0].__length__()

    def i_print(self, name: list[any]):
        for i in name:
            tp = type(i).__name__
            if tp == 'Number':
                print(i.number, end='')
            elif tp == 'String':
                print(i.string, end='')
            else:
                print(name, end='')

    def visit_function_node(self, node: FunctionDefineNode):
        args = node.params
        name = node.name 
        body = node.body 
        self.context.add(name, Function(name, args, body))

    def visit(self, node):
        kind = type(node).__name__
        if kind == 'FunctionDefineNode':
            self.visit_function_node(node)
            return
        if kind == 'BinOpNode':
            return self.visit_bin_op_node(node)
        if kind == 'ReturnNode':
            return self.visit_return_node(node)
        if kind == 'BreakNode':
            return self.visit_break_node()
        if kind == 'ContinueNode':
            return self.visit_continue_node()
        if kind == 'NoneNode':
            return self.visit_null_node()
        if kind == 'NumberNode':
            return Number(node.num)
        if kind == 'MemberAccessNode' or kind == "str":
            return self.visit_member_access(node).copy()
        if kind == 'BoolNode':
            if node.bol == 'false':
                return Bool(False)
            return Bool(True)
        if kind == 'VarDefineNode':
            return self.visit_var_define_node(node)
        if kind == 'ArrayNode':
            return self.visit_array_node(node)
        if kind == 'IfNode':
            tmp = self.visit_if_node(node)
            if tmp is None: return 
            if type(tmp).__name__ == 'ReturnSignal': return tmp
            return 
        if kind == 'WhileNode':
            tmp = self.visit_while_node(node)
            if tmp is None: return 
            if type(tmp).__name__ == 'ReturnSignal': return tmp 
            return
        if kind == 'ForLoopNode':
            tmp = self.visit_for_loop_node(node)
            if tmp is None: return 
            if type(tmp).__name__ == 'ReturnSignal': return tmp 
            return 
        if kind == 'IncNode':
            return self.visit_inc_node(node)
        if kind == 'DecNode':
            return self.visit_dec_node(node)
        if kind == 'ElementGetNode':
            return self.visit_element_get_node(node)
        if kind == 'BitNotNode':
            return Number(~int(self.visit(node.value).number))
        if kind == 'StringNode':
            return String(node.string)
        if kind == 'NewNode':
            return self.visit_new_node(node)
        if kind == 'CallNode':
            return self.visit_call_node(node)
        if kind == 'AssignNode':
            return self.visit_assign_node(node)
        if kind == 'ClassNode':
            cn = self.visit_class_node(node)
            self.context.add(cn.name, cn)
            return
        raise SystemError(f'Operator not supposed "{kind}"')
    
    def visit_null_node(self):
        return Null()
    
    def visit_class_node(self, node: ClassNode):
        name = node.name 
        fie  = node.fields
        return StructTemplate(name, fie)

    def visit_new_node(self, node: NewNode):
        name = node.name
        args = node.args
        t: StructTemplate = self.context.get(name)
        tmp = {}
        for i in args:
            if type(t.fields.get(i, NameNotFound())).__name__ == 'NameNotFound':
                raise NameError(f'Name "{i}" not found in class "{name}"') 
            tmp[i] = self.visit(args[i])
        return Struct(name, tmp)

    def visit_element_get_node(self, node: ElementGetNode):
        id = node.name
        pos = self.visit(node.pos)
        return self.visit(id).__get_element__(pos)

    def visit_call_node(self, node: CallNode):
        if type(node.name).__name__ == 'MemberAccessNode':
            name = node.name.fiele
            parent = node.name.parent
            id = self.visit_member_access(name)
            this = self.visit_member_access(parent)
            param: list[VarDefineNode] = id.param
            body: BlockNode  = id.body
            context_ = {}
            context_['this'] = this 
            for i in range(len(node.param)):
                context_[param[i].name] = self.visit(node.param[i])
            return Interpreter(body.codes, Context(context_, self.context, id.name)).res  
        id: Function = self.visit_member_access(node.name)
        if type(id).__name__ == 'function' or type(id).__name__ == 'method':
            vals = []
            for i in node.param:
                vals.append(self.visit(i))
            return id(vals)
        param: list[VarDefineNode] = id.param
        body: BlockNode  = id.body
        context_ = {}
        for i in range(len(node.param)):
            context_[param[i].name] = self.visit(node.param[i])
        return Interpreter(body.codes, Context(context_, self.context, id.name)).res

    def visit_member_access(self, node):
        if type(node).__name__ == 'ElementGetNode':
            return self.visit_element_get_node(node)
        if type(node).__name__ == 'str':
            return self.context.get(node)
        parent = node.parent
        field_ = node.fiele
        if type(parent).__name__ == 'str':
            return self.context.get(parent).__field_get__(field_)
        return self.visit_member_access(parent).__field_get__(field_)

    def visit_var_define_node(self, node):
        name_ = node.name
        init_value = node.init_value
        if init_value is not None:
            init_value = self.visit(init_value)
        self.context.add(name_, init_value)

    def visit_array_node(self, node):
        val = []
        for i in node.elements:
            val.append(self.visit(i))
        return Array(val)
    
    def visit_break_node(self):
        return BreakSignal()
    
    def visit_return_node(self, node: ReturnNode):
        self.res = self.visit(node.value)
        return ReturnSignal()
    
    def visit_continue_node(self, node: ContinueNode):
        return ContinueSignal()
    
    def visit_block_node(self, node: BlockNode):
        codes = node.codes
        pc    = 0
        while pc < len(codes):
            i = codes[pc]
            pc += 1
            tp = type(self.visit(i)).__name__
            if tp in ('ReturnSignal', 'ContinueSignal', 'BreakSignal'):
                return tp
        return None

    def visit_if_node(self, node: IfNode):
        self.create_new_context()
        cond = self.visit(node.condition)
        body = node.if_true
        el   = node._else
        if cond.bol: 
            tmp = self.visit_block_node(body)
            self.leave_context()
            return tmp 
        elif not cond.bol and el is not None: 
            tmp = self.visit_block_node(el)
            self.leave_context()
            return tmp

    def create_new_context(self, name = 'NewScope'):
        self.context = Context({}, self.context, name)

    def leave_context(self):
        if self.context.parent is None:
            raise Exception('no scope to leave')
        self.context = self.context.parent

    def visit_for_loop_node(self, node: ForLoopNode):
        self.create_new_context('<ForLoop>')
        self.visit(node.init)
        cond: Bool = self.visit(node.is_loop)
        while cond.bol:
            body = self.visit_block_node(node.body)
            self.visit(node.change)
            cond = self.visit(node.is_loop)
            if body == 'ReturnSignal':
                return ReturnSignal()
            if body == 'ContinueSignal':
                continue
            if body == 'BreakSignal':
                break 
        self.leave_context()

    def visit_inc_node(self, node: IncNode):
        tp = node.kind
        if type(node.id).__name__ == 'ElementGetNode':
            if tp == SEL_PRE:
                tmp = self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).added_by(Number(1.0))
                self.visit_member_access(node.id.name).__set_elemeny__(
                        self.visit(node.id.pos),
                        tmp
                    )
                return tmp
            else:
                tmp = self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).copy()
                self.visit_member_access(node.id.name).__set_elemeny__(
                    self.visit(node.id.pos),
                    self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).added_by(Number(1.0))
                )
                return tmp
        else:
            if tp == SEL_PRE:
                tmp = self.visit(node.id).added_by(Number(1.0))
                self.context.set(node.id, tmp)
                return tmp
            else:
                tmp = self.visit(node.id).copy()
                self.context.set(node.id, self.visit(node.id).added_by(Number(1.0)))
                return tmp

    def visit_assign_node(self, node: AssignNode):
        if type(node.id).__name__ == 'MemberAccessNode':
            self.visit_member_access(node.id).__iset__(self.visit(node.value).copy())
        elif type(node.id).__name__ == 'ElementGetNode':
            self.visit_member_access(node.id.name).__set_elemeny__(self.visit(node.id.pos), self.visit(node.value).copy())
        else:
            self.context.set(node.id, self.visit(node.value).copy())

    def visit_dec_node(self, node: DecNode):
        tp = node.kind
        if type(node.id).__name__ == 'ElementGetNode':
            if tp == SEL_PRE:
                tmp = self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).subbed_by(Number(1.0))
                self.visit_member_access(node.id.name).__set_elemeny__(
                        self.visit(node.id.pos),
                        tmp
                    )
                return tmp
            else:
                tmp = self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).copy()
                self.visit_member_access(node.id.name).__set_elemeny__(
                    self.visit(node.id.pos),
                    self.visit_member_access(node.id.name).__get_element__(self.visit(node.id.pos)).subbed_by(Number(1.0))
                )
                return tmp
        else:
            if tp == SEL_PRE:
                tmp = self.visit(node.id).subbed_by(Number(1.0))
                self.context.set(node.id, tmp)
                return tmp
            else:
                tmp = self.visit(node.id).copy()
                self.context.set(node.id, self.visit(node.id).subbed_by(Number(1.0)))
                return tmp

    def visit_while_node(self, node: WhileNode):
        self.create_new_context('<WhileLoop>')
        cond: Bool = self.visit(node.condition)
        while cond.bol:
            body = self.visit_block_node(node.body)
            cond = self.visit(node.condition)
            if body == 'ReturnSignal':
                return ReturnSignal()
            if body == 'ContinueSignal':
                continue
            if body == 'BreakSignal':
                break 
        self.leave_context() 

    def visit_bin_op_node(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        if op == '+': return left.added_by(right)
        if op == '-': return left.subbed_by(right)
        if op == '*': return left.muled_by(right)
        if op == '/': return left.dived_by(right)
        if op == '<<': return left.left_move(right)
        if op == '>>': return left.right_move(right)
        if op == '**': return Number(left.number ** right.number)
        if op == 'and': return left.__cond_and__(right)
        if op == 'or': return left.__cond_or__(right)
        if op == '>': return left.__comp_big__(right)
        if op == '<': return left.__comp_less__(right)
        if op == '>=': return left.__comp_big_or_eq__(right)
        if op == '<=': return left.__comp_less_or_eq__(right)
        if op == '%': return left.__modd__(right)
        if op == '!=': return left.__comp_neq__(right)
        if op == '==': return left.__comp_eq__(right)