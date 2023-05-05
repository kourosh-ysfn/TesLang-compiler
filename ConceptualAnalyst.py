class ProgTableNode:
    def __init__(self) -> None:
        self.functions = []
        
    def addFunc(self, funcNode) -> None:
        self.functions.append(funcNode)


class FunctionTableNode:
    def __init__(self) -> None:
        self.name = None
        self.flist = None
        self.returnType = None
    
    def setName(self, iden) -> None:
        self.name = iden
    
    def setReturnType(self, returnType) -> None:
        self.returnType = returnType
    
    def setFlist(self, flist) -> None:
        self.flist = flist

class BodyTableNode:
    def __init__(self) -> None:
        self.stmts = []

    def addStmt(self, stmt) -> None:
        self.stmts.append(stmt)

class StmtTableNode:
    def __init__(self) -> None:
        self.types = []
        self.nodes = []

    def addTypeOfNode(self, typeOfNode) -> None:
        self.types.append(typeOfNode)

    def addNode(self, node) ->None:
        self.nodes.append(node)

class DefVarNode:
    def __init__(self) -> None:
        self.type = None
        self.name = None
        self.value = None

    def addTypeOfNode(self, typeOfNode) -> None:
        self.type = typeOfNode

    def addNameOfNode(self, name) -> None:
        self.name = name
    
    def addValueOfNode(self, value) -> None:
        self.value = value

class FlistNode:
    def __init__(self) -> None:
        self.varNames = []
        self.types = []
        self.pointer_to_other_flist = None
    
    def addVarName(self, name) -> None:
        self.varNames.append(name)
    
    def addTypeOfVar(self, vartype) -> None:
        self.types.append(vartype)
    
    def pointToFlist(self, pointer_to_other_flist):
        self.pointer_to_other_flist = pointer_to_other_flist


class ExprTableNode:
    def __init__(self) -> None:
        self.first_expr = None
        self.second_expr = None
        self.type_of_operation = None

    def addFirstNode(self, first_expr) -> None:
        self.first_expr = first_expr
    
    def addSecondNode(self, second_expr2) -> None:
        self.second_expr = second_expr2
    
    def addTypeOfOp(self, type_of_operation) -> None:
        self.type_of_operation = type_of_operation
    

class ClistTableNode:
    def __init__(self) -> None:
        self.expr = None
        self.clist = None

    def addExpr(self, expr) -> None:
        self.expr = expr
    
    def pointToClist(self, clist) -> None:
        self.clist = clist