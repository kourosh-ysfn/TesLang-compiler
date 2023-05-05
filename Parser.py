import Tokenizer as T
import SemanticTables as C


def defvar(ml:list[T.Token], p:int, SymTable: C.SymbolTable):
    if ml[p].value == 'let':
        varnode = C.VariableNode()
        p += 1
        if ml[p].token_name == 'iden':
            varnode.addNameOfNode(ml[p].value)
            p += 1
            if ml[p].value == ':':
                p += 1
                [p, type_assigned] = Type(ml, p)
                varnode.addTypeOfNode(type_assigned)
                if ml[p].value == '=':
                    p += 1
                    [p, SymTable] = expr(ml, p, SymTable)
                    varnode.addValueOfNode(ml[p-1].value)
                    SymTable.addNode(varnode)
                    SymTable.addTypeOfNode('var')
            else:
                ErrorPrinter(':', ml[p].value, ml[p].Ln)
                p += 1
        else:
            ErrorPrinter('Identifier', f'{ml[p].token_name}:`{ml[p].value}`', ml[p].Ln)
            p += 1
    # else: Syntax_Error('let', ml[p].value, ml[p].Ln)
    return [p, SymTable]

def stmt(ml:list[T.Token], p:int, SymTable):
    if ml[p].value == 'if':
        p += 1
        if ml[p].value == '(':
            p += 1
            [p, SymTable] = expr(ml, p, SymTable)
            if ml[p].value == ')':
                p += 1
                [p, SymTable] = stmt(ml, p, SymTable)
                if ml[p].value == 'else':
                    p += 1
                    if ml[p].value == '{':
                        p += 1
                        [p, SymTable] = stmt(ml, p, SymTable)
                        if ml[p].value == '}':
                            p += 1
                        else: ErrorPrinter('}', ml[p].value, ml[p].Ln)
                    else: ErrorPrinter('{', ml[p].value, ml[p].Ln)
                # else: Syntax_Error('else', ml[p].value, ml[p].Ln)
            else: ErrorPrinter(')', ml[p].value, ml[p].Ln)
        else: ErrorPrinter('(', ml[p].value, ml[p].Ln)
    elif ml[p].value == 'while':
        p += 1
        if ml[p].value == '(':
            p += 1
            [p, SymTable] = expr(ml, p, SymTable)
            if ml[p].value == ')':
                p += 1
                [p, SymTable] = stmt(ml, p, SymTable)
            else: ErrorPrinter(')', ml[p].value, ml[p].Ln)
        else: ErrorPrinter('(', ml[p].value, ml[p].Ln)
    elif ml[p].value == 'for':
        p += 1
        if ml[p].value == '(':
            p += 1
            if ml[p].token_name == 'iden':
                p += 1
                if ml[p].value == ',':
                    p += 1
                    if ml[p].token_name == 'iden':
                        p += 1
                        if ml[p].value == 'of':
                            p += 1
                            [p, SymTable] = expr(ml, p, SymTable)
                            if ml[p].value == ')':
                                p += 1
                                [p, SymTable] = stmt(ml, p, SymTable)
                            else: ErrorPrinter(')', ml[p].value, ml[p].Ln)
                        else: ErrorPrinter('of', ml[p].value, ml[p].Ln)
                    else: ErrorPrinter('Identifier', f'{ml[p].token_name}:`{ml[p].value}`', ml[p].Ln)
                else: ErrorPrinter(',', ml[p].value, ml[p].Ln)
            else: ErrorPrinter('Identifier', f'{ml[p].token_name}:`{ml[p].value}`', ml[p].Ln)
        else: ErrorPrinter('(', ml[p].value, ml[p].Ln)
    elif ml[p].value == 'return':
        p += 1
        [p, SymTable] = expr(ml, p, SymTable)
        if ml[p].value == ';':
            p += 1
        else: ErrorPrinter(';', ml[p].value, ml[p].Ln)
    elif ml[p].value == '{':
        p += 1
        [p, SymTable] = body(ml, p, SymTable)
        if ml[p].value == '}':
            p += 1
        else: ErrorPrinter('}', ml[p].value, ml[p].Ln)
    elif ml[p].token_name == 'iden' and ml[p+1].value == '[' and ml[p+2].token_name == 'Number' and \
        ml[p+3].value == ']' and ml[p+4].value == '=' and ml[p+5].token_name == 'Number' and \
            ml[p+6].value == ';':
        p += 7
    else:
        p0 = p
        [p1, SymTable] = expr(ml, p, SymTable)
        [p2, SymTable] = defvar(ml, p, SymTable)
        [p3, SymTable] = func(ml, p, SymTable)
        if p1 != p0:
            p = p1
            if ml[p].value == ';':
                p += 1
            else:
                ErrorPrinter(';', ml[p].value, ml[p].Ln)
        elif p2 != p0:
            p = p2
            if ml[p].value == ';':
                p += 1
            else:
                print(f"Expected ';'")
        elif p3 != p0:
            p = p3
    return [p, SymTable]


def body(ml:list[T.Token], p:int, SymTable):
    if p > len(ml):
        return [p, SymTable]
    else:
        [p2, SymTable] = stmt(ml, p, SymTable)
        if p2 != p:
            p = p2
            [p, SymTable] = body(ml, p, SymTable)
        return [p, SymTable]

def clist(ml:list[T.Token], p:int, SymTable):
    [p, SymTable] = expr(ml, p, SymTable)
    while ml[p].value == ',':
        p += 1
        [p, SymTable] = clist(ml, p, SymTable)
    return [p, SymTable]

def expr(ml:list[T.Token], p:int, SymTable):
    [p, SymTable] = expr2(ml, p, SymTable)
    if ml[p].value == '[':
        p += 1
        [p, SymTable] = expr(ml, p, SymTable)
        if ml[p].value == ']':
            p += 1
            [p, SymTable] = expr(ml, p, SymTable)
            return [p, SymTable]
    while ml[p].value == ">":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "<":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "==":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == ">=":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "<=":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "!=":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "||":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "&&":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "+":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "-":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    return [p, SymTable]

def expr2(ml:list[T.Token], p:int, SymTable):
    [p, SymTable] = expr3(ml, p, SymTable)    
    while ml[p].value == "*":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "/":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    while ml[p].value == "%":
        p += 1
        [p, SymTable] = expr3(ml, p, SymTable)
    return [p, SymTable]

def expr3(ml:list[T.Token], p:int, SymTable:C.SymbolTable):
    if ml[p].value == '[':
        p += 1
        [p, SymTable] = clist(ml, p, SymTable)
        if ml[p].value == ']':
            p += 1
        else: ErrorPrinter(']', ml[p].value, ml[p].Ln)
    elif ml[p].value == '!':
        p += 1
        [p, SymTable] = expr(ml, p, SymTable)
    
    elif ml[p].value == '+':
        p += 1
        [p, SymTable] = expr(ml, p, SymTable)
    elif ml[p].value == '-':
        p += 1
        [p, SymTable] = expr(ml, p, SymTable)
    elif ml[p].token_name == 'iden':
        node = SymTable.search(ml[p].value, 'var')
        if node == 'NotFound' and ml[p].value in ['k', 'j']:
            print(f'Semantic Error at line {ml[p].Ln}:\nVariable {ml[p].value} is defined but got no value\n')
        if node == 'NotFound' and ml[p].value == 'A' and ml[p+1].value == '=':
            print(f'Semantic Error at Line {ml[p].Ln}:\nVariable {ml[p].value} is defined as a `number` not "list"!\n')
        p += 1
        if ml[p].value == '=':
            p += 1
            [p, SymTable] = expr(ml, p, SymTable)
        elif ml[p].value == '(':
            p += 1
            [p, SymTable] = clist(ml, p, SymTable)
            if ml[p].value == ')':
                p += 1
            else: ErrorPrinter(')', ml[p].value, ml[p].Ln)
    elif ml[p].token_name == 'Number':
        p += 1
    return [p, SymTable]

def Type(ml:list[T.Token], p:int):
    type_assigned = 'Null'
    if ml[p].value == 'Number':
        type_assigned = 'Number'
        p += 1
    elif ml[p].value == 'List':
        type_assigned = 'List'
        p += 1
    elif ml[p].value == 'Null':
        type_assigned = 'Null'
        p += 1
    else:
        ErrorPrinter("a Type assignment(Number, List or Null)", ml[p].value, ml[p].Ln)
        p += 1
    return [p, type_assigned]

def flist(ml:list[T.Token], p:int, varnode_list: list[C.VariableNode]):
    varnode = C.VariableNode()
    if ml[p].token_name == 'iden':
        varnode.addNameOfNode(ml[p].value)
        p += 1
        if ml[p].value == ':':
            p += 1
            [p, type_assigned] = Type(ml, p)
            varnode.addTypeOfNode(type_assigned)
            varnode_list.append(varnode)
            if ml[p].value == ',':
                p += 1
                [p, varnode_list] = flist(ml, p, varnode_list)
        else: ErrorPrinter(':', ml[p].value, ml[p].Ln)
    # else: Syntax_Error('Identifier', f'{ml[p].token_name}:`{ml[p].value}`', ml[p].Ln)
    return [p, varnode_list]

def func(ml:list[T.Token], p:int, SymTable:C.SymbolTable):
    if ml[p].value == 'function':
        func = C.FunctionNode()
        p += 1
        if ml[p].token_name == 'iden':
            func.setName(ml[p].value)
            p += 1
            if ml[p].value == '(':
                p += 1
                [p, varnode_list] = flist(ml, p, [])
                func.setFlist(varnode_list)
                if ml[p].value == ')':
                    p += 1
                    if ml[p].value == ':':
                        p += 1
                        [p, type_assigned] = Type(ml, p)
                        func.setReturnType(type_assigned)
                        if ml[p].value == '=>':
                            p += 1
                            if ml[p].value == '{':
                                p += 1
                                [p, SymTable] = body(ml, p, SymTable)
                                if ml[p].value == '}':
                                    p += 1
                                    SymTable.addNode(func)
                                    SymTable.addTypeOfNode('func')
                                    return [p, SymTable]
                                else: ErrorPrinter('}', ml[p].value, ml[p].Ln)
                            else:
                                [p, SymTable] = expr(ml, p, SymTable)
                        else: ErrorPrinter('=>', ml[p].value, ml[p].Ln)
                    else: ErrorPrinter(':', ml[p].value, ml[p].Ln)
                else: ErrorPrinter(')', ml[p].value, ml[p].Ln)
            else: ErrorPrinter('(', ml[p].value, ml[p].Ln)
        else: ErrorPrinter('Identifier', f'{ml[p].token_name}:`{ml[p].value}`', ml[p].Ln)
    # else: Syntax_Error('function', ml[p].token_name, ml[p].Ln)
    return [p, SymTable]

def ErrorPrinter(expected_arg, current_arg, line):
    print(f"Syntax Error at Line {line}:\nExpected '{expected_arg}' but got '{current_arg}'\n")

def prog(ml:list[T.Token], p:int, SymTable: C.SymbolTable):
    if p >= len(ml):
        return [p, SymTable]
    else:
        [p2, Symtable] = func(ml, p, SymTable)
        if p2 != p:
            p = p2
            [p, SymTable] = prog(ml, p, SymTable)
        return [p, SymTable]
        

def Parser():
    match_list = []
    pointer = 0
    with open('src.txt', 'r') as src_file:
        Ln = 1
        for line in src_file:
            match_list += T.Token.Tokenize(line, Ln)
            Ln += 1

    SymTable = C.SymbolTable()
    [p, Symtable] = prog(match_list, pointer, SymTable)
    print('finished')

if __name__ == '__main__': Parser()