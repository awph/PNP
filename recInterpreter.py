import AST
import copy
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
    '+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
    '*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
    '%': lambda x, y: x%y,
}

conditional_operator = {
    '==': lambda x, y: x == y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
}

vars = {}
dwg = None
step = 0


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
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


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operator[self.op], args)


@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()


@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.IfNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.ForNode)
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
    if 'c' in arguments:
        center = arguments.pop('c')
        arguments['cx'] = center.pop('x')
        arguments['cy'] = center.pop('y')
    if 'size' in arguments:
        arguments['font-size'] = arguments.pop('size')
    if 'font' in arguments:
        arguments['font-family'] = arguments.pop('font')

    shape = None

    if shape_type.upper() == 'LINE':
        shape = shapes.Line()
        if 'width' in arguments:
            arguments['stroke-width'] = arguments.pop('width')
        if 'fill' in arguments:
            arguments['stroke'] = arguments.pop('fill')
        if 'p1' in arguments:
            p1 = arguments.pop('p1')
            arguments['x1'] = p1.pop('x')
            arguments['y1'] = p1.pop('y')
        if 'p2' in arguments:
            p1 = arguments.pop('p2')
            arguments['x2'] = p1.pop('x')
            arguments['y2'] = p1.pop('y')
        print(arguments)
    elif shape_type.upper() == 'CIRCLE':
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
        if 'close' in arguments and arguments.pop('close') == True:
            shape = shapes.Polygon(points)
        else:
            shape = shapes.Polyline(points)


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
        color = arguments[1].execute()
        if color[0:1] == '#':
            return '%s' % arguments[1].execute()
        else:
            return '#%s' % arguments[1].execute()
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
    if self.nbargs == 0:
        return self.children[0].execute()
    else:
        args = [c.execute() for c in self.children]
        return reduce(conditional_operator[self.operator], args)

def displayMenu(files):
    examples = ' | '.join(files)

    print('')
    print('')
    print('-----------------------------------------------')
    print('--------- Welcome -- PNP Compiler -------------')
    print('-----------------------------------------------')
    print('-------------- Alexandre Perez & Mirco Nasuti -')
    print('')
    print('Compile a PNP file by typing: compile <filepath>')
    print('Exit by typing: exit')
    print('')
    print('You can try some examples by typing : ')
    print('compile examples/'+examples)


def compile(filepath):
    import os
    if not os.path.exists(filepath):
        print("File not found")
        return
    global dwg
    filename = os.path.basename(filepath)[:-4]
    print('start compiling: ' + filename)
    prog = open(filepath).read()
    vars = {}
    dwg = drawing.Drawing(filename=filename+'.svg', debug=False, profile='tiny')
    ast = parse(prog)
    ast.execute()
    dwg.save()
    print('Compiled and saved in: ' + filename + '.svg')

# http://stackoverflow.com/a/2605125
class Discarder(object):
    def write(self, text):
        pass # do nothing

if __name__ == "__main__":
    import sys
    # discard output
    oldstdout = sys.stdout
    oldstderr = sys.stderr
    sys.stdout = Discarder()
    sys.stderr = Discarder()
    from parse import parse
    sys.stdout = oldstdout
    sys.stderr = oldstderr

    if len(sys.argv) > 1:
        compile(sys.argv[1])
        sys.exit(0)

    path = 'examples/'
    ext = 'pnp'
    from os import listdir
    from os.path import isfile, join
    files = [ f for f in listdir(path) if isfile(join(path,f)) and f[-3:].upper() == ext.upper() ]

    inputValue = ''
    while not inputValue.__eq__('exit'):
        displayMenu(files)
        inputValue = input('PNP > ')
        if inputValue.startswith('compile '):
            try:
                compile(inputValue[8:])
            except:
                print("Error:", sys.exc_info()[0])