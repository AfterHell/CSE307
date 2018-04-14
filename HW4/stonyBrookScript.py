import re
errorFlag = 0 #0 == no syntax error
#Encapsulation fuctions for wrapping lexToken

#1. For only storing data
class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class NumberNode(Node):
    def __init__(self, v):
        if('.' in v):
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value

class BoolNode(Node):
    def __init__(self, v):
        if(v == 'True'):
            self.value = True
        elif(v=='False'):
            self.value = False

    def evaluate(self):
        return self.value

class ListNode(Node):
    def __init__(self, s):
        self.list1 = [s]
        self.list2 = []
    def evaluate(self):
        for statement in self.list1:
            self.list2.append(statement.evaluate())
        return self.list2

class EmptyListNode(Node):
    def __init__(self):
        self.list1 = []

    def evaluate(self):
        return self.list1

class StringNode(Node):
    def __init__(self, v):
        self.value = str(v).replace('"','').replace("'","")

    def evaluate(self):
        return self.value

#########################

#2. For manipulating data
class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '+'):
            return self.v1.evaluate() + self.v2.evaluate()
        elif (self.op == '-'):
            return self.v1.evaluate() - self.v2.evaluate()

        elif (self.op == '*'):
            if(isinstance(self.v1, NumberNode) and isinstance(self.v2, NumberNode)):
                return self.v1.evaluate() * self.v2.evaluate()
            else:
                raise TypeError

        elif (self.op == '/'):
            return self.v1.evaluate() / self.v2.evaluate()
        elif (self.op == '//'):
            return self.v1.evaluate() // self.v2.evaluate()
        elif (self.op == '%'):
            return self.v1.evaluate() % self.v2.evaluate()
        
class PowerNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        return self.v1.evaluate() ** self.v2.evaluate()
        


class PrintNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):        
        self.value = self.value.evaluate()
        if(isinstance(self.value, str)):
            print("'"+self.value+"'")
        else:
            print(self.value)

class BlockNode(Node):
    def __init__(self, s):
        self.sl = [s]

    def execute(self):
        for statement in self.sl:
            statement.execute()

class IndexingNode(Node):
    def __init__(self, list1, index):
        self.list1 = list1
        self.index = index

    def evaluate(self):
        return self.list1.evaluate()[self.index.evaluate()]

class BooleanNode(Node):
    def __init__(self, op, v1, v2):
        self.op = op
        self.v1 = v1
        self.v2 = v2
    def evaluate(self):
        if(self.op == 'or'):
            if(isinstance(self.v1.evaluate(), bool)and isinstance(self.v2.evaluate(), bool)):
                return self.v1.evaluate() or self.v2.evaluate()
            else:
                raise TypeError
        elif(self.op == 'and'):
            if(isinstance(self.v1.evaluate(), bool)and isinstance(self.v2.evaluate(), bool)):
                return self.v1.evaluate() and self.v2.evaluate()
            else:
                raise TypeError



        elif(self.op == '<'):
            return self.v1.evaluate() < self.v2.evaluate()
        elif(self.op == '<='):
            return self.v1.evaluate() <= self.v2.evaluate()
        elif(self.op == '=='):
            return self.v1.evaluate() == self.v2.evaluate()
        elif(self.op == '<>'):
            return self.v1.evaluate() != self.v2.evaluate()
        elif(self.op == '>'):
            return self.v1.evaluate() > self.v2.evaluate()
        elif(self.op == '>='):
            return self.v1.evaluate() >= self.v2.evaluate()
        elif(self.op == 'in'):
            return self.v1.evaluate() in self.v2.evaluate()

class NotNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        if(isinstance(self.v.evaluate(), bool)):
            return not self.v.evaluate()
        else:
            raise TypeError
###################






#Token identifiers section
tokens = (
    'LPAREN', 'RPAREN',
    'NUMBER', 'STRING',
    'PLUS','MINUS','TIMES','DIVIDE',
    'OR','AND','NOT','LESSTHAN','LESSEQUALTHAN','EQUAL','NOTEQUAL','GREATERTHAN',
    'GREATEREQUALTHAN','IN','FLOORDIVIDE','MODULUS','POWER','LBRACKET', 'RBRACKET',
    'COMMA','TRUE','FALSE'
    )


# Tokens' literal representation-> get a string, return the a token with same value
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_OR = r'or'
t_AND = r'and'
t_NOT = r'not'
t_LESSTHAN = r'<'
t_LESSEQUALTHAN = r'<='
t_EQUAL = r'=='
t_NOTEQUAL = r'<>'
t_GREATERTHAN = r'>'
t_GREATEREQUALTHAN = r'>='
t_IN = r'in'
t_FLOORDIVIDE = r'//'
t_MODULUS = r'%'
t_POWER = r'\*\*'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

#get a string, return a node contains that string instead of the original string
def t_NUMBER(t):
    r'-?\d*(\d\.|\.\d)\d* | \d+'
    try:
        t.value = NumberNode(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\'[^\']*\'|\"[^"]*\"'
    try:
        t.value = StringNode(t.value)
    except ValueError:
        print("String value is invalid %d", t.value)
        t.value = ""
    return t

def t_TRUE(t):
    r'True'
    try:
        t.value = BoolNode(t.value)
    except ValueError:
        print("Bool value is invalid %d", t.value)
        t.value = ""
    return t

def t_FALSE(t):
    r'False'
    try:
        t.value = BoolNode(t.value)
    except ValueError:
        print("Bool value is invalid %d", t.value)
        t.value = ""
    return t


# Ignored characters
t_ignore = " \t"

def t_error(t):
    global errorFlag
    errorFlag = 1
    print("SYNTAX ERROR")
    

# Build the parser
import ply.lex as lex
parser = lex.lex()









# Parsing rules
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','NOT'),
    ('left','LESSTHAN','LESSEQUALTHAN','EQUAL','NOTEQUAL','GREATERTHAN','GREATEREQUALTHAN'),
    ('left', 'IN'),
    ('left','PLUS','MINUS'),
    ('left','FLOORDIVIDE'),
    ('left','MODULUS'),
    ('left','TIMES','DIVIDE'),
    ('right','POWER'),
    ('left','LBRACKET','RBRACKET'),
    ('left','LPAREN','RPAREN'),
    )

#1
def p_block(t):
    """
    block :  print_smt 
    """
    t[0] = t[1]

#2
def p_print_smt(t):
    """
    print_smt : expression  
    """
    t[0] = PrintNode(t[1])



#3456
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression FLOORDIVIDE expression
                  | expression MODULUS expression'''

    t[0] = BopNode(t[2], t[1], t[3])

#7
def p_expression_powerOp(t):
    '''expression : expression POWER expression'''

    t[0] = PowerNode(t[1], t[3])


#8
def p_expression_parent(t):
    '''expression : LPAREN expression RPAREN'''
                  
    t[0] = t[2]

#9
def p_expression_list(t):
    '''expression : LBRACKET list RBRACKET'''
                  
    t[0] = t[2]

#10
def p_expression_emptyList(t):
    '''expression : LBRACKET RBRACKET'''
                  
    t[0] = EmptyListNode()

#11
def p_expression_list_indexing(t):
    '''expression : expression LBRACKET expression RBRACKET'''
                  
    t[0] = IndexingNode(t[1],t[3])

#12
def p_expression_booleanOp(t):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression LESSTHAN expression
                  | expression LESSEQUALTHAN expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression GREATERTHAN expression
                  | expression GREATEREQUALTHAN expression
                  | expression IN expression'''
    t[0] = BooleanNode(t[2], t[1], t[3])

#13
def p_expression_notOp(t):
    '''expression : NOT expression'''
    t[0] = NotNode(t[2])









#14 I remove the comma by -> in tokenizing part, if i detect comma, i return nothing
#from right to left, we always have last element added to the list first
#e.g. list-> ex list-> ex ex list -> ex ex ex ex list-> 
#       ex ex ex ex -> ex ex ex list -> ex ex list -> ex list -> list
def p_list_expression_list(t):
    '''list :  expression COMMA list '''

    t[0] = t[3]
    t[0].list1.insert(0,t[1])

#15 #if there are more than 1 elements, 14 will run the first
def p_list_expression(t):
    '''list :  expression '''
                  
    t[0] = ListNode(t[1])





#16
def p_expression_factor(t):
    '''expression : factor'''
    t[0] = t[1]


#17
def p_factor_number(t):
    '''factor : NUMBER
              | STRING  
              | TRUE
              | FALSE'''
    t[0] = t[1]



def p_error(t):
    print("SYNTAX ERROR")
    global errorFlag
    errorFlag = 1
    #parser.token()
    raise SyntaxError



import ply.yacc as yacc
yacc.yacc()

import sys

def main():
    
    global errorFlag

    if (len(sys.argv) != 2):
       sys.exit("invalid arguments")
    fd = open(sys.argv[1], 'r')

    code = ""
    for line in fd:
        code = line.strip()

        try:
            lex.input(code)
            while True:
                token = lex.token()
                if not token: 
                    break
                    
                #print(token)
        
            ast = yacc.parse(code)
            ast.execute()
            

        except Exception:
            if(errorFlag == 0):
                print("SEMANTIC ERROR")
        
        errorFlag = 0

        

main()
