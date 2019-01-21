import json
def to_json(string):
	l = [""]
	dl = {'text':'','bold':False,'italic':False,'underline':False,'obfuscated':False,'strike':False}
	curr = ''
	nextIsColorCode = False
	for i in string:
		if i == '&':
			nextIsColorCode = True
		elif nextIsColorCode:
			dl['text'] = curr
			curr = ''
			l.append(dl)
			dl['text'] = ''
			nextIsColorCode = False
			if i == 'l':
				dl['bold'] = not dl['bold']
			if i == 'o':
				dl['italic'] = not dl['italic']
			if i == 'k':
				dl['obfuscated'] = not dl['obfuscated']
			if i == 'm':
				dl['strike'] = not dl['strike']
			if i == 'n':
				dl['underline'] = not dl['underline']

		else:
			curr += i
	dl['text'] = curr
	curr = ''
	l.append(dl)
	print('JSON',l)
	return l