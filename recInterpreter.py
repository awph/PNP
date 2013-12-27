import AST, copy
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
dwg = None
step = 0

@addToClass(AST.ProgramNode)# Done
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)# Done
def execute(self):
    if isinstance(self.tok, str) and not self.real_string:
        if self.tok.upper() == 'STEP':
            return step
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
    for x in range(self.children[0].execute(), self.children[1].execute()):
        self.children[2].execute()
        global step
        step = x

@addToClass(AST.ApplyNode)
def execute(self):
    transformation = self.children[0].execute()
    for shape in self.children[1].execute():
        if transformation.type.upper() == 'ROTATE':
            shape.rotate(transformation['angle'], (transformation['c']['x'], transformation['c']['y']))
        elif transformation.type.upper() == 'SCALE':
            shape.scale(transformation['sx'], transformation['sy'])
        elif transformation.type.upper() == 'TRANSLATE':
            shape.translate(transformation['p'][0]['x'], transformation['p'][0]['y'])
        elif transformation.type.upper() == 'HIDE':
            shape['visibility'] = 'hidden' if transformation['h'] else 'visible'
            dwg.add(shape.copy())


@addToClass(AST.ArgumentNode)
def execute(self):
    if len(self.children) > 1:
        args = [c.execute() for c in self.children]
    else:
        args = self.children[0].execute()
    return [self.key, args]

@addToClass(AST.ArgumentsNode)
def execute(self):
    arguments = {}
    for argument in self.children:
        if argument.execute()[0] == 'p':
            if 'p' in arguments:
                arguments[argument.execute()[0]].append(argument.execute()[1])
            else:
                arguments[argument.execute()[0]] = [argument.execute()[1]]
        else:
            arguments[argument.execute()[0]] = argument.execute()[1]
    return arguments

@addToClass(AST.ShapeNode)
def execute(self):
    shape_type = self.children[0].execute()
    arguments = copy.deepcopy(self.children[1].execute())
    if 'fill_color' in arguments:
        arguments['fill'] = arguments.pop('fill_color')
    if 'border_width' in arguments:
        arguments['stroke-width'] = arguments.pop('border_width')
    if 'border_color' in arguments:
        arguments['stroke'] = arguments.pop('border_color')
    shape = None
    if shape_type.upper() == 'LINE':
        shape = shapes.Line()
    elif shape_type.upper() == 'CIRCLE':
        if 'c' in arguments:
            center = arguments.pop('c')
            arguments['cx'] = center.pop('x')
            arguments['cy'] = center.pop('y')
        shape = shapes.Circle()
    elif shape_type.upper() == 'RECT':
        if 'o' in arguments:
            center = arguments.pop('o')
            arguments['x'] = center.pop('x')
            arguments['y'] = center.pop('y')
        shape = shapes.Rect()
    elif shape_type.upper() == 'ELLIPSE':
        shape = shapes.Ellipse()
    elif shape_type.upper() == 'CUSTOMSHAPE':
        points = []
        for point in arguments.pop('p'):
            points.append((point.pop('x'), point.pop('y')))
        shape = shapes.Polygon(points)
    elif shape_type.upper() == 'TEXT':
        shape = text.Text(arguments.pop('content'))
        if 'p' in arguments:
            center = arguments.pop('p')[0]
            arguments['x'] = center.pop('x')
            arguments['y'] = center.pop('y')
    else:
        print("Error: shape type %s undefined!" % shape_type)

    shape.update(arguments)
    return shape

@addToClass(AST.PointNode)
def execute(self):
    arguments = self.children[0].execute()
    return {'x': arguments["x"], 'y': arguments["y"]}

@addToClass(AST.ColorNode)
def execute(self):
    arguments = self.children[1].execute()
    type = arguments[0].execute().upper()
    if type == 'NAME':
        return arguments[1].execute()
    elif type == 'HEX':
        return 'hex(%s)' % arguments[1].execute()
    elif type == 'RGB':
        return "rgb(%d,%d,%d)" % (int(arguments[1][0].execute()), int(arguments[1][1].execute()), int(arguments[1][2].execute()))

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
        return reduce(conditional_operator[self.operator], args)

if __name__ == "__main__":
    from parse import parse
    import sys

    path = 'Tests/'
    ext = '.pnp'
    files = ['clock', 'comboTest1', 'comboTest2', 'comboTest3', 'customShapeTest', 'helloTest', 'ifTest', 'loopTest', 'loopTest2', 'rotationTest', 'rotationTest2', 'simpleShapesTest', 'someTransforms']

    for file in files:
        print('--------------------------------------')
        print('--------- start ' + file + ' -------------')
        print('--------------------------------------')
        fullpath = path + file + ext
        prog = open(fullpath).read()
        vars ={}
        dwg = drawing.Drawing(filename=file+'.svg', debug=False, profile='tiny')
        ast = parse(prog)
        ast.execute()
        dwg.save()