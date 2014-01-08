__author__ = 'Alexandre'

import ply.lex as lex

reserved_words = (
	'color',
	'point',
	'line',
	'circle',
	'rect',
	'ellipse',
	'customshape',
	'text',
	'rotate',
	'scale',
	'translate',
	'hide',
	'if',
	'while',
	'for',
	'step',
	'apply',
    'rgb',
    'hex',
    'name',
    'x',
    'y',
    'p1',
    'p2',
    'fill_color',
    'border_color',
    'width',
    'c',
    'r',
    'border_width',
    'o',
    'height',
    'rx',
    'ry',
    'p',
    'close',
    'content',
    'font',
    'size',
    'angle',
    'sx',
    'sy',
    'h',
)

tokens = (
	'INTEGER',
	'BOOLEAN',
	'STRING',
    'ADD_OP',
    'MUL_OP',
    'COND_OP',
    'IDENTIFIER'
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '():,;={}'

def t_INTEGER(token):
	r'[+-]?\d+'
	try:
		token.value = int(token.value)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (token.lineno,token.value))
		token.value = 0
	return token

def t_BOOLEAN(token):
	r'(YES|NO)'
	try:
		token.value = token.value == 'YES'
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (token.lineno,token.value))
		token.value = 0
	return token

def t_STRING(token):
	r'"(?:[^"\\]|\\.)*"'
	try:
		token.value = str(token.value)[1:-1]
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (token.lineno,token.value))
		token.value = ""
	return token

def t_ADD_OP(token):
	r'[+-]'
	return token

def t_MUL_OP(token):
	r'[*/%]'
	return token

def t_COND_OP(token):
	r'(==|<=|>=|<|>)'
	return token

def t_IDENTIFIER(token):
	r'[A-Za-z_]\w*'
	if token.value in reserved_words:
		token.type = token.value.upper()
	return token

def t_newline(token):
	r'\n+'
	token.lexer.lineno += len(token.value)

t_ignore  = ' \t'

def t_error(token):
	print ("Illegal character '%s'" % repr(token.value[0]))
	token.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))