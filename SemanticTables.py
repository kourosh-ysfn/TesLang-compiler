class FunctionNode:
    def __init__(self) -> None:
        self.name = None
        self.flist = None
        self.return_type = None
    
    def setName(self, iden) -> None:
        self.name = iden
    
    def setReturnType(self, return_type) -> None:
        self.return_type = return_type
    
    def setFlist(self, flist) -> None:
        self.flist = flist


class VariableNode:
    def __init__(self) -> None:
        self.type = None
        self.name = None
        self.value = None

    def addTypeOfNode(self, type_of_var) -> None:
        self.type = type_of_var

    def addNameOfNode(self, name) -> None:
        self.name = name
    
    def addValueOfNode(self, value) -> None:
        self.value = value

class SymbolTable:
    def __init__(self) -> None:
        self.nodes = []
        self.types = []

    def addNode(self, node):
        self.nodes.append(node)
    
    def addTypeOfNode(self, type_of_var):
        self.types.append(type_of_var)
    
    def search(self, name, type_of_node):
        for i in range(len(self.types)):
            if self.types[i] == type_of_node:
                if self.nodes[i].name == name:
                    return self.nodes[i]
        return 'NotFound'