from pygments import highlight, lexers, formatters

def pjs(inJSON):
	colorful_json = highlight(str(inJSON), lexers.JsonLexer(), formatters.TerminalFormatter())
	print(colorful_json)
