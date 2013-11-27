__author__ = 'Alexandre'

import ply.yacc as yacc

from lex import tokens
import AST

def p_color_arguments(p):
    ''' color_arguments : RGB '(' IDENTIFIER ',' IDENTIFIER ',' IDENTIFIER ')'
							| RGB '(' INTEGER ',' IDENTIFIER ',' IDENTIFIER ')'
							| RGB '(' IDENTIFIER ',' INTEGER ',' IDENTIFIER ')'
							| RGB '(' IDENTIFIER ',' IDENTIFIER ',' INTEGER ')'
							| RGB '(' INTEGER ',' INTEGER ',' IDENTIFIER ')'
							| RGB '(' INTEGER ',' IDENTIFIER ',' INTEGER ')'
							| RGB '(' IDENTIFIER ',' INTEGER ',' INTEGER ')'
							| RGB '(' INTEGER ',' INTEGER ',' INTEGER ')'
							| HEX '(' IDENTIFIER ')'
							| HEX '(' STRING ')'
							| NAME '(' IDENTIFIER ')'
							| NAME '(' STRING ')'
    '''
    key = p[1]
    value = []
    i = 3
    while str(p[i]) != ')':
        value[i-3] = p[i]
        i+=1
    p[0] = AST.ArgumentNode([key, value])

def p_point_arguments(p):
    ''' point_arguments : X '(' IDENTIFIER ')'
							| X '(' INTEGER ')'
							| Y '(' IDENTIFIER ')'
							| Y '(' INTEGER ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_point_arguments_rec(p):
    ''' point_arguments : X '(' IDENTIFIER ')' ':' point_arguments
							| X '(' INTEGER ')' ':' point_arguments
							| Y '(' IDENTIFIER ')' ':' point_arguments
							| Y '(' INTEGER ')' ':' point_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_line_arguments(p):
    ''' line_arguments : P1 '(' IDENTIFIER ')'
						| P1 '(' POINT ')'
						| P2 '(' IDENTIFIER ')'
						| P2 '(' POINT ')'
						| FILL_COLOR '(' IDENTIFIER ')'
						| FILL_COLOR '(' COLOR ')'
						| WIDTH '(' IDENTIFIER ')'
						| WIDTH '(' INTEGER ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_line_arguments_rec(p):
    ''' line_arguments : P1 '(' IDENTIFIER ')' ':' line_arguments
						| P1 '(' POINT ')' ':' line_arguments
						| P2 '(' IDENTIFIER ')' ':' line_arguments
						| P2 '(' POINT ')' ':' line_arguments
						| FILL_COLOR '(' IDENTIFIER ')' ':' line_arguments
						| FILL_COLOR '(' COLOR ')' ':' line_arguments
						| WIDTH '(' IDENTIFIER ')' ':' line_arguments
						| WIDTH '(' INTEGER ')' ':' line_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_circle_arguments(p):
    ''' circle_arguments :  C '(' IDENTIFIER ')'
							| C '(' POINT ')'
							| R '(' IDENTIFIER ')'
							| R '(' INTEGER ')'
							| BORDER_COLOR '(' IDENTIFIER ')'
							| BORDER_COLOR '(' COLOR ')'
							| BORDER_WIDTH '(' IDENTIFIER ')'
							| BORDER_WIDTH '(' INTEGER ')'
							| FILL_COLOR '(' IDENTIFIER ')'
							| FILL_COLOR '(' COLOR ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_circle_arguments_rec(p):
    ''' circle_arguments :  C '(' IDENTIFIER ')' ':' circle_arguments
                            | C '(' POINT ')' ':' circle_arguments
                            | R '(' IDENTIFIER ')' ':' circle_arguments
                            | R '(' INTEGER ')' ':' circle_arguments
                            | BORDER_COLOR '(' IDENTIFIER ')' ':' circle_arguments
                            | BORDER_COLOR '(' COLOR ')' ':' circle_arguments
                            | BORDER_WIDTH '(' IDENTIFIER ')' ':' circle_arguments
                            | BORDER_WIDTH '(' INTEGER ')' ':' circle_arguments
                            | FILL_COLOR '(' IDENTIFIER ')' ':' circle_arguments
                            | FILL_COLOR '(' COLOR ')' ':' circle_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_rect_arguments(p):
    ''' rect_arguments :  O '(' IDENTIFIER ')'
                        | O '(' POINT ')'
                        | WIDTH '(' IDENTIFIER ')'
                        | WIDTH '(' INTEGER ')'
                        | HEIGHT '(' IDENTIFIER ')'
                        | HEIGHT '(' INTEGER ')'
                        | RX '(' IDENTIFIER ')'
                        | RX '(' INTEGER ')'
                        | RY '(' IDENTIFIER ')'
                        | RY '(' INTEGER ')'
                        | BORDER_COLOR '(' IDENTIFIER ')'
                        | BORDER_COLOR '(' COLOR ')'
                        | BORDER_WIDTH '(' IDENTIFIER ')'
                        | BORDER_WIDTH '(' INTEGER ')'
                        | FILL_COLOR '(' IDENTIFIER ')'
                        | FILL_COLOR '(' COLOR ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_rect_arguments_rec(p):
    ''' rect_arguments :  O '(' IDENTIFIER ')' ':' rect_arguments
                        | O '(' POINT ')' ':' rect_arguments
                        | WIDTH '(' IDENTIFIER ')' ':' rect_arguments
                        | WIDTH '(' INTEGER ')' ':' rect_arguments
                        | HEIGHT '(' IDENTIFIER ')' ':' rect_arguments
                        | HEIGHT '(' INTEGER ')' ':' rect_arguments
                        | RX '(' IDENTIFIER ')' ':' rect_arguments
                        | RX '(' INTEGER ')' ':' rect_arguments
                        | RY '(' IDENTIFIER ')' ':' rect_arguments
                        | RY '(' INTEGER ')' ':' rect_arguments
                        | BORDER_COLOR '(' IDENTIFIER ')' ':' rect_arguments
                        | BORDER_COLOR '(' COLOR ')' ':' rect_arguments
                        | BORDER_WIDTH '(' IDENTIFIER ')' ':' rect_arguments
                        | BORDER_WIDTH '(' INTEGER ')' ':' rect_arguments
                        | FILL_COLOR '(' IDENTIFIER ')' ':' rect_arguments
                        | FILL_COLOR '(' COLOR ')' ':' rect_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_ellipse_arguments(p):
    ''' ellipse_arguments :  C '(' IDENTIFIER ')'
							| C '(' POINT ')'
							| RY '(' IDENTIFIER ')'
							| RY '(' INTEGER ')'
							| RX '(' IDENTIFIER ')'
							| RX '(' INTEGER ')'
							| BORDER_COLOR '(' IDENTIFIER ')'
							| BORDER_COLOR '(' COLOR ')'
							| BORDER_WIDTH '(' IDENTIFIER ')'
							| BORDER_WIDTH '(' INTEGER ')'
							| FILL_COLOR '(' IDENTIFIER ')'
							| FILL_COLOR '(' COLOR ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_ellipse_arguments_rec(p):
    ''' ellipse_arguments :  C '(' IDENTIFIER ')' ':' ellipse_arguments
							| C '(' POINT ')' ':' ellipse_arguments
							| RY '(' IDENTIFIER ')' ':' ellipse_arguments
							| RY '(' INTEGER ')' ':' ellipse_arguments
							| RX '(' IDENTIFIER ')' ':' ellipse_arguments
							| RX '(' INTEGER ')' ':' ellipse_arguments
							| BORDER_COLOR '(' IDENTIFIER ')' ':' ellipse_arguments
							| BORDER_COLOR '(' COLOR ')' ':' ellipse_arguments
							| BORDER_WIDTH '(' IDENTIFIER ')' ':' ellipse_arguments
							| BORDER_WIDTH '(' INTEGER ')' ':' ellipse_arguments
							| FILL_COLOR '(' IDENTIFIER ')' ':' ellipse_arguments
							| FILL_COLOR '(' COLOR ')' ':' ellipse_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_shape_arguments(p):
    ''' shape_arguments :  P '(' IDENTIFIER ')'
                            | P '(' POINT ')'
                            | BORDER_COLOR '(' IDENTIFIER ')'
                            | BORDER_COLOR '(' COLOR ')'
                            | BORDER_WIDTH '(' IDENTIFIER ')'
                            | BORDER_WIDTH '(' INTEGER ')'
                            | CLOSE '(' IDENTIFIER ')'
                            | CLOSE '(' BOOLEAN ')'
                            | FILL_COLOR '(' IDENTIFIER ')'
                            | FILL_COLOR '(' COLOR ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_shape_arguments_rec(p):
    ''' shape_arguments :  P '(' IDENTIFIER ')' ':' shape_arguments
							| P '(' POINT ')' ':' shape_arguments
							| BORDER_COLOR '(' IDENTIFIER ')' ':' shape_arguments
							| BORDER_COLOR '(' COLOR ')' ':' shape_arguments
							| BORDER_WIDTH '(' IDENTIFIER ')' ':' shape_arguments
							| BORDER_WIDTH '(' INTEGER ')' ':' shape_arguments
							| CLOSE '(' IDENTIFIER ')' ':' shape_arguments
							| CLOSE '(' BOOLEAN ')' ':' shape_arguments
							| FILL_COLOR '(' IDENTIFIER ')' ':' shape_arguments
							| FILL_COLOR '(' COLOR ')' ':' shape_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_text_arguments(p):
    ''' text_arguments :  CONTENT '(' IDENTIFIER ')'
                        | CONTENT '(' INTEGER ')'
                        | P '(' IDENTIFIER ')'
                        | P '(' INTEGER ')'
                        | FONT '(' IDENTIFIER ')'
                        | FONT '(' INTEGER ')'
                        | SIZE '(' IDENTIFIER ')'
                        | SIZE '(' INTEGER ')'
                        | FILL_COLOR '(' IDENTIFIER ')'
                        | FILL_COLOR '(' COLOR ')'
    '''
    p[0] = AST.ArgumentsNode(AST.ArgumentNode([p[1], p[3]]))

def p_text_arguments_rec(p):
    ''' text_arguments :  CONTENT '(' IDENTIFIER ')' ':' text_arguments
                        | CONTENT '(' INTEGER ')' ':' text_arguments
                        | P '(' IDENTIFIER ')' ':' text_arguments
                        | P '(' INTEGER ')' ':' text_arguments
                        | FONT '(' IDENTIFIER ')' ':' text_arguments
                        | FONT '(' INTEGER ')' ':' text_arguments
                        | SIZE '(' IDENTIFIER ')' ':' text_arguments
                        | SIZE '(' INTEGER ')' ':' text_arguments
                        | FILL_COLOR '(' IDENTIFIER ')' ':' text_arguments
                        | FILL_COLOR '(' COLOR ')' ':' text_arguments
    '''
    p[0] = AST.ArgumentsNode([AST.ArgumentNode([p[1], p[3]]), p[6]])

def p_shape(p):
    ''' shape : COLOR ':' color_arguments
                | POINT ':' point_arguments
                | LINE ':' line_arguments
                | CIRCLE ':' circle_arguments
                | RECT ':' rect_arguments
                | ELLIPSE ':' ellipse_arguments
                | SHAPE ':' shape_arguments
                | TEXT ':' text_arguments
    '''

def p_assign(p):
    ''' assignation : IDENTIFIER '=' type '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")