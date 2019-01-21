import json
def to_json(string):
	l = [""]
	dl = {'text':'','bold':False,'italic':False,'underline':False,'obfuscated':False,'strike':False,'color':'white'}
	curr = ''
	nextIsColorCode = False
	for i in string:
		if i == '&':
			nextIsColorCode = True
		elif nextIsColorCode:
			dl['text'] = curr
			curr = ''
			l.append(dl.copy())
			dl['text'] = ''
			nextIsColorCode = False
			if i == 'l':
				dl['bold'] = not dl['bold']
			elif i == 'o':
				dl['italic'] = not dl['italic']
			elif i == 'k':
				dl['obfuscated'] = not dl['obfuscated']
			elif i == 'm':
				dl['strike'] = not dl['strike']
			elif i == 'n':
				dl['underline'] = not dl['underline']
			elif i == "4":
				dl['color'] = "dark_red"
			elif i == "c":
				dl['color'] = "red"
			elif i == "6":
				dl['color'] = "gold"
			elif i == "e":
				dl['color'] = "yellow"
			elif i == "2":
				dl['color'] = "dark_green"
			elif i == "a":
				dl['color'] = "green"
			elif i == "b":
				dl['color'] = "aqua"
			elif i == "3":
				dl['color'] = "dark_aqua"
			elif i == "1":
				dl['color'] = "dark_blue"
			elif i == "9":
				dl['color'] = "blue"
			elif i == "d":
				dl['color'] = "light_purple"
			elif i == "5":
				dl['color'] = "dark_purple"
			elif i == "f":
				dl['color'] = "white"
			elif i == "7":
				dl['color'] = "gray"
			elif i == "8":
				dl['color'] = "dark_gray"
			elif i == "0":
				dl['color'] = "black"
			elif i == "r":
				dl = {**dl,**{'bold':False,'italic':False,'underline':False,'obfuscated':False,'strike':False,'color':'white'}}
		else:
			curr += i
	dl['text'] = curr
	curr = ''
	l.append(dl)
	print('l',l)
	print('JSON',l)
	return l