__author__ = 'Alexandre'

import ply.yacc as yacc

from lex import tokens
import AST

def p_program_statement(p):
    ''' program : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_program_rec(p):
    ''' program : statement program '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_statement(p):
    ''' statement : assignation
                    | transformation
                    | control '''
    p[0] = p[1]

def p_integer_argument(p):
    ''' integer_argument : IDENTIFIER
                        | INTEGER
                        | STEP
    '''
    p[0] = AST.TokenNode(p[1])

def p_integer_argument_operator(p):
    ''' integer_argument : integer_argument ADD_OP integer_argument
                        | integer_argument MUL_OP integer_argument
    '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_string_argument(p):
    ''' string_argument : IDENTIFIER
                        | STRING
    '''
    p[0] = AST.TokenNode(p[1])

def p_point_argument(p):
    ''' point_argument : IDENTIFIER
                        | POINT
    '''
    p[0] = AST.TokenNode(p[1])

def p_color_argument(p):
    ''' color_argument : IDENTIFIER
                        | COLOR
    '''
    p[0] = AST.TokenNode(p[1])

def p_boolean_argument(p):
    ''' boolean_argument : IDENTIFIER
                        | BOOLEAN
    '''
    p[0] = AST.TokenNode(p[1])

def p_color_arguments(p):
    ''' color_arguments : RGB '(' integer_argument ',' integer_argument ',' integer_argument ')'
							| HEX '(' string_argument ')'
							| NAME '(' string_argument ')'
    '''
    key = p[1]
    value = []
    if len(p) == 5:
        value = p[3]
    elif len(p) == 9:
        value = [p[3], p[5], p[7]]
    p[0] = AST.ArgumentNode(AST.TokenNode(key), value) #TODO:

def p_point_arguments(p):
    ''' point_arguments : X '(' integer_argument ')'
                        | Y '(' integer_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_point_arguments_rec(p):
    ''' point_arguments : X '(' integer_argument ')' ':' point_arguments
                        | Y '(' integer_argument ')' ':' point_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_line_arguments(p):
    ''' line_arguments : P1 '(' point_argument ')'
						| P2 '(' point_argument ')'
						| FILL_COLOR '(' color_argument ')'
						| WIDTH '(' integer_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_line_arguments_rec(p):
    ''' line_arguments : P1 '(' point_argument ')' ':' line_arguments
						| P2 '(' point_argument ')' ':' line_arguments
						| FILL_COLOR '(' color_argument ')' ':' line_arguments
						| WIDTH '(' integer_argument ')' ':' line_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_circle_arguments(p):
    ''' circle_arguments :  C '(' point_argument ')'
							| R '(' integer_argument ')'
							| BORDER_COLOR '(' color_argument ')'
							| BORDER_WIDTH '(' integer_argument ')'
							| FILL_COLOR '(' color_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_circle_arguments_rec(p):
    ''' circle_arguments :  C '(' point_argument ')' ':' circle_arguments
                            | R '(' integer_argument ')' ':' circle_arguments
                            | BORDER_COLOR '(' color_argument ')' ':' circle_arguments
                            | BORDER_WIDTH '(' integer_argument ')' ':' circle_arguments
                            | FILL_COLOR '(' color_argument ')' ':' circle_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_rect_arguments(p):
    ''' rect_arguments :  O '(' point_argument ')'
                        | WIDTH '(' integer_argument ')'
                        | HEIGHT '(' integer_argument ')'
                        | RX '(' integer_argument ')'
                        | RY '(' integer_argument ')'
                        | BORDER_COLOR '(' color_argument ')'
                        | BORDER_WIDTH '(' integer_argument ')'
                        | FILL_COLOR '(' color_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_rect_arguments_rec(p):
    ''' rect_arguments :  O '(' point_argument ')' ':' rect_arguments
                        | WIDTH '(' integer_argument ')' ':' rect_arguments
                        | HEIGHT '(' integer_argument ')' ':' rect_arguments
                        | RX '(' integer_argument ')' ':' rect_arguments
                        | RY '(' integer_argument ')' ':' rect_arguments
                        | BORDER_COLOR '(' color_argument ')' ':' rect_arguments
                        | BORDER_WIDTH '(' integer_argument ')' ':' rect_arguments
                        | FILL_COLOR '(' color_argument ')' ':' rect_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_ellipse_arguments(p):
    ''' ellipse_arguments :  C '(' point_argument ')'
							| RY '(' integer_argument ')'
							| RX '(' integer_argument ')'
							| BORDER_COLOR '(' color_argument ')'
							| BORDER_WIDTH '(' integer_argument ')'
							| FILL_COLOR '(' color_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_ellipse_arguments_rec(p):
    ''' ellipse_arguments :  C '(' point_argument ')' ':' ellipse_arguments
							| RY '(' integer_argument ')' ':' ellipse_arguments
							| RX '(' integer_argument ')' ':' ellipse_arguments
							| BORDER_COLOR '(' color_argument ')' ':' ellipse_arguments
							| BORDER_WIDTH '(' integer_argument ')' ':' ellipse_arguments
							| FILL_COLOR '(' color_argument ')' ':' ellipse_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_customshape_arguments(p):
    ''' customshape_arguments :  P '(' point_argument ')'
                                | BORDER_COLOR '(' color_argument ')'
                                | BORDER_WIDTH '(' integer_argument ')'
                                | CLOSE '(' boolean_argument ')'
                                | FILL_COLOR '(' color_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_customshape_arguments_rec(p):
    ''' customshape_arguments :  P '(' point_argument ')' ':' customshape_arguments
							| BORDER_COLOR '(' color_argument ')' ':' customshape_arguments
							| BORDER_WIDTH '(' integer_argument ')' ':' customshape_arguments
							| CLOSE '(' boolean_argument ')' ':' customshape_arguments
							| FILL_COLOR '(' color_argument ')' ':' customshape_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_text_arguments(p):
    ''' text_arguments :  CONTENT '(' string_argument ')'
                        | P '(' point_argument ')'
                        | FONT '(' string_argument ')'
                        | SIZE '(' integer_argument ')'
                        | FILL_COLOR '(' color_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_text_arguments_rec(p):
    ''' text_arguments :  CONTENT '(' string_argument ')' ':' text_arguments
                        | P '(' point_argument ')' ':' text_arguments
                        | FONT '(' string_argument ')' ':' text_arguments
                        | SIZE '(' integer_argument ')' ':' text_arguments
                        | FILL_COLOR '(' color_argument ')' ':' text_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_color(p):
    ''' color : COLOR ':' color_arguments '''
    p[0] = AST.ColorNode([AST.TokenNode(p[1]), p[3]])

def p_point(p):
    ''' point : POINT ':' point_arguments '''
    p[0] = AST.PointNode(p[3])

def p_line(p):
    ''' line : LINE ':' line_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_circle(p):
    ''' circle : CIRCLE ':' circle_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_rect(p):
    ''' rect : RECT ':' rect_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_ellipse(p):
    ''' ellipse : ELLIPSE ':' ellipse_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_customshape(p):
    ''' customshape : CUSTOMSHAPE ':' customshape_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_text(p):
    ''' text : TEXT ':' text_arguments '''
    p[0] = AST.ShapeNode([AST.TokenNode(p[1]), p[3]])

def p_shape(p):
    ''' shape : line
                | circle
                | rect
                | ellipse
                | customshape
                | text
    '''
    p[0] = p[1]

def p_rotate_arguments(p):
    ''' rotate_arguments : ANGLE '(' integer_argument ')'
                            | C '(' point_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_rotate_arguments_rec(p):
    ''' rotate_arguments : ANGLE '(' integer_argument ')' ':' rotate_arguments
                            | C '(' point_argument ')' ':' rotate_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_scale_arguments(p):
    ''' scale_arguments : SX '(' integer_argument ')'
                        | SY '(' integer_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_scale_arguments_rec(p):
    ''' scale_arguments : SX '(' integer_argument ')' ':' scale_arguments
                        | SY '(' integer_argument ')' ':' scale_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])] + p[6].children)

def p_translate_arguments(p):
    ''' translate_argument : P '(' point_argument ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode(p[1], p[3]))

def p_hide_arguments(p):
    ''' hide_argument : H '(' boolean_argument ')'
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode(p[1], p[3])])

def p_transformation(p):
    ''' transformation : ROTATE ':' rotate_arguments
						| SCALE ':' scale_arguments
						| TRANSLATE ':' translate_argument
						| HIDE ':' hide_argument
    '''
    p[0] = AST.TransformationNode([AST.TokenNode(p[1]), p[3]])

def p_control_if(p):
    ''' control : IF condition '{' program '}' '''
    p[0] = AST.IfNode([p[2], p[4]])

def p_control_while(p):
    ''' control : WHILE condition '{' program '}' '''
    p[0] = AST.WhileNode([p[2], p[4]])

def p_control_for(p):
    ''' control : FOR integer_argument ':' integer_argument '{' program '}' '''
    p[0] = AST.ForNode([p[2], p[4], p[6]])

def p_apply_body(p):
    ''' apply_body : IDENTIFIER ';'
    '''
    p[0] = AST.ApplyBodyNode([AST.TokenNode(p[1])])

def p_apply_body_rec(p):
    ''' apply_body : IDENTIFIER ';' apply_body
    '''
    p[0] = AST.ApplyBodyNode([AST.TokenNode(p[1])] + p[3].children)

def p_control_apply(p):
    ''' control : APPLY IDENTIFIER '{' apply_body '}' '''
    p[0] = AST.ApplyNode([AST.TokenNode(p[2]), p[4]])

def p_condition(p):
    ''' condition : integer_argument COND_OP integer_argument
                | string_argument COND_OP string_argument
                | boolean_argument
    '''
    p[0] = AST.ConditionalNode(p[2], [p[1], p[3]])

def p_assign(p):
    ''' assignation : IDENTIFIER '=' shape ';'
                    | IDENTIFIER '=' point ';'
                    | IDENTIFIER '=' color ';'
                    | IDENTIFIER '=' transformation ';'
                    | IDENTIFIER '=' integer_argument ';'
                    | IDENTIFIER '=' string_argument ';'
                    | IDENTIFIER '=' point_argument ';'
                    | IDENTIFIER '=' color_argument ';'
                    | IDENTIFIER '=' boolean_argument ';'
    '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        if p.type in tokens:
            print ("Syntax error in line %d, %s token is reserved word" % (p.lineno, p.type))
        else:
            print ("Syntax error in line %d" % p.lineno)
            print (p)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


def parse(program):
    return yacc.parse(program, debug=1)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
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
        result = yacc.parse(prog)
        if result:
            print(result)
            import os
            graph = result.makegraphicaltree()
            name = os.path.splitext(fullpath)[0]+'-ast.pdf'
            graph.write_pdf(name)
            print ("wrote ast to", name)
        else:
            print ("Parsing returned no result!")
            exit(-1)