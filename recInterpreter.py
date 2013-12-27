import AST
from svgwrite import text, shapes, drawing
from AST import addToClass
from functools import reduce
from lex import reserved_words

class Transformation:
    def __init__(self, type):
        self.type = type
        self.arguments = {}

    def __setitem__(self, key, value):
        self.arguments[key] = value

    def add_arguments(self, arguments):
        for key in arguments:
            self[key] = arguments[key]

    def __getitem__(self, item):
        return self.arguments[item]


operator = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

conditional_operator = {
    '==' : lambda x,y: x==y,
    '<=' : lambda x,y: x<=y,
    '>=' : lambda x,y: x>=y,
    '<' : lambda x,y: x<y,
    '>' : lambda x,y: x>y,
}

vars ={}
shapes_to_draw = []

@addToClass(AST.ProgramNode)# Done
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)# Done
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            if self.tok in reserved_words:
                return self.tok
            else:
                print("Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)# Done
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operator[self.op], args)

@addToClass(AST.AssignNode)# Done
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.WhileNode)# Done
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.IfNode)# Done
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.ForNode)#TODO step
def execute(self):
    for x in range(self.children[0], self.children[1]):
        self.children[2].execute()

@addToClass(AST.ApplyNode)
def execute(self):
    transformation = self.children[0].execute()
    for shape in self.children[1].execute():
        if transformation.type.upper() == 'ROTATE':
            shape.rotate(transformation.getArgument('angle'), (transformation.getArgument('c')[0], transformation.getArgument('c')[1]))
        elif transformation.type.upper() == 'SCALE':
            shape.scale(transformation.getArgument('sx'), transformation.getArgument('sy'))
        elif transformation.type.upper() == 'TRANSLATE':
            shape.translate(transformation.getArgument('p')[0], transformation.getArgument('p')[1])
        elif transformation.type.upper() == 'HIDE':
            shape['visibility'] = 'hidden' if transformation['h'] else 'visible'


@addToClass(AST.ArgumentNode)
def execute(self):
    return [self.key, self.children[0].execute()]

@addToClass(AST.ArgumentsNode)
def execute(self):
    arguments = {}
    for argument in self.children:
        arguments[argument.execute()[0]] = argument.execute()[1]
    return arguments

@addToClass(AST.ShapeNode)
def execute(self):
    shape_type = self.children[0].execute()
    arguments = self.children[1].execute()
    shape = None
    if shape_type.upper() == 'LINE':
        shape = shapes.Line()
    elif shape_type.upper() == 'CIRCLE':
        shape = shapes.Circle()
    elif shape_type.upper() == 'RECT':
        shape = shapes.Rect()
    elif shape_type.upper() == 'ELLIPSE':
        shape = shapes.Ellipse()
    elif shape_type.upper() == 'CUSTOMSHAPE':
        shape = shapes.Polygon()
    elif shape_type.upper() == 'TEXT':
        shape = text.Text(arguments.pop('content'))
        center = arguments.pop('p')
        arguments['x'] = center.pop('x')
        arguments['y'] = center.pop('y')
    else:
        print("Error: shape type %s undefined!" % shape_type)

    print(type(shape))
    shape.update(arguments)
    shapes_to_draw.append(shape)
    return shape

@addToClass(AST.PointNode)
def execute(self):
    arguments = self.children[0].execute()
    return {'x' : arguments["x"], 'y': arguments["y"]}

@addToClass(AST.ColorNode)
def execute(self):
    arguments = self.children[0].execute()
    return arguments

@addToClass(AST.TransformationNode)
def execute(self):
    transformation = Transformation(self.children[0].tok)
    transformation.add_arguments(self.children[1].execute())
    return transformation

@addToClass(AST.ApplyBodyNode)
def execute(self):
    shapes = []
    for shape in self.children:
        shapes.append(shape.execute())
    return shapes

@addToClass(AST.ConditionalNode)
def execute(self):
    if self.nbargs == 1:
        return self.children[0].execute()
    else:
        args = [c.execute() for c in self.children]
        return reduce(operator[self.op], args)

if __name__ == "__main__":
    from parse import parse
    import sys

    path = 'Tests/'
    ext = '.pnp'
    files = ['clock', 'comboTest1', 'comboTest2', 'comboTest3', 'customShapeTest', 'helloTest', 'ifTest', 'loopTest', 'loopTest2', 'rotationTest', 'rotationTest2', 'simpleShapesTest', 'someTransforms']
    files = ['helloTest']

    for file in files:
        print('--------------------------------------')
        print('--------- start ' + file + ' -------------')
        print('--------------------------------------')
        fullpath = path + file + ext
        prog = open(fullpath).read()
        ast = parse(prog)
        ast.execute()

        dwg = drawing.Drawing(filename=file+'.svg', debug=False, profile='tiny')
        for shape in shapes_to_draw:
            dwg.add(shape)
        dwg.save()