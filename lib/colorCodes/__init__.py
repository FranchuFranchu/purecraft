"""
This library implements basic mc color codes, plus a few more:
&i:
	a&ib&i when you shift-click a, the content of your chat box is replaced by "b"
&g: click actions
	&gs:
		a&gub&i: like &i, but without shift
	&gu:
		go to xkcd&guxkcd.com&g: goes to http://xkcd.com
	&gr:
		creative&gr/gm 1&g: changes mode to creative. can also be used to send chat
	&gp:
		go to page 42&gp42&g: in a book, it changes the page to 42
&h:
	hi&hhow are you&h: when hi is hovered, "How are you" is shown

"""

import json
def to_json(string):
	l = [""]
	dl = {'text':'','clickEvent':{"action":"","value":"" },'hoverEvent':{"action":"","value":"" },'bold':False,'italic':False,'underline':False,'obfuscated':False,'strike':False,'color':'white'}
	curr = ''
	nextIsColorCode = False
	nextIsClick = False
	nextIsHover = False
	compData = ''
	isCurrentlyInsertingText = False
	for i in string:
		if i == '&':
			nextIsColorCode = True
		elif nextIsClick:
			if i == 'u':
				dl['clickEvent']['action'] = 'open_url'
			elif i == 'r':
				dl['clickEvent']['action'] = 'run_command'
			elif i == 's':
				dl['clickEvent']['action'] = 'suggest_command'
			elif i == 'p':
				dl['clickEvent']['action'] = 'change_page'
			nextIsClick = False
			isCurrentlyInsertingText = True

		elif nextIsHover:
			dl['hoverEvent']['action'] = 'show_text'
			isCurrentlyInsertingText = True
			nextIsHover = False
		elif nextIsColorCode:
			i = i.lower()
			if i == "i":
				if isCurrentlyInsertingText:
					dl['insertion'] = compData
					compData = ''
					isCurrentlyInsertingText = False
					
				else:
					isCurrentlyInsertingText = True
			elif i == 'g': #click events
				if isCurrentlyInsertingText:	
					if dl['clickEvent']['action'] == 'change_page':
						try:
							compData = int(compData)
						except ValueError:
							compData = 1
					elif dl['clickEvent']['action'] == 'open_url':
						if not(compData.startswith('http://') or compData.startswith('https://')):
							compData = 'http://'+compData
					dl['clickEvent']['value'] = compData
					compData = ''
				nextIsClick = not nextIsClick
				isCurrentlyInsertingText = False
			elif i == 'h':
				if isCurrentlyInsertingText:	
					dl['hoverEvent']['value'] = compData
					compData = ''
				nextIsHover = not nextIsHover
				isCurrentlyInsertingText = False
			else:
				dl['text'] = curr
				curr = ''
				l.append(dl.copy())
				dl['text'] = ''
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
			nextIsColorCode = False

		elif isCurrentlyInsertingText:
			compData+=i
		else:
			curr += i
	dl['text'] = curr
	curr = ''
	l.append(dl)
	for i in l:
		if type(i) == dict:
			if i['clickEvent'] == {"action":"","value":"" }:
				del l[l.index(i)]['clickEvent']
			if i['hoverEvent'] == {"action":"","value":"" }:
				del l[l.index(i)]['hoverEvent']

			if i['bold'] == False:
				del l[l.index(i)]['bold']
			if i['italic'] == False:
				del l[l.index(i)]['italic']
			if i['obfuscated'] == False:
				del l[l.index(i)]['obfuscated']
			if i['strike'] == False:
				del l[l.index(i)]['strike']
			if i['underline'] == False:
				del l[l.index(i)]['underline']
			if i['color'] == 'white':
				del l[l.index(i)]['color']
			if i['text'] == '':
				del l[l.index(i)]
	print('Message converted to JSON',l)
	return l