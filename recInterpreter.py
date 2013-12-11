import AST
from AST import addToClass
from functools import reduce
operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

vars ={}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)
	
@addToClass(AST.ArgumentNode)
def execute(self):
	
@addToClass(AST.ArgumentsNode)
def execute(self):
	
@addToClass(AST.ShapeNode)
def execute(self):
	
@addToClass(AST.TransformationNode)
def execute(self):
	
@addToClass(AST.IfNode)
def execute(self):
	if self.children[0].execute():
		self.children[1].execute();
		
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()
		
@addToClass(AST.ForNode)
def execute(self):
	for x in range(self.children[0], self.children[1]):
		self.children[2].execute();

@addToClass(AST.ApplyBodyNode)
def execute(self):
	
@addToClass(AST.ApplyNode)
def execute(self):
	
@addToClass(AST.ConditionalNode)
def execute(self):
	
@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

if __name__ == "__main__":
    from parser5 import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    
    ast.execute()