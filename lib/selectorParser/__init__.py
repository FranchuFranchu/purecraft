def parse(string,caller,world):

	print('aaa')

	"""
	try:
		
		if ncaller.isProtocol:
			caller = ncaller.world.entities[ncaller.eid]
			world = ncaller.world
	except AttributeError:
		pass
	"""
	assert caller.isEntity # should be true if the caller is an Entity
	print('s',string)
	if string.startswith('@'):
		print('@')
		listOfPossible = set() # set of entity ids
		if string[1] == 's': # @s
			return set([caller])
		elif string[1] == 'a':
			for i in world.players:
				listOfPossible.add(i.eid)
		elif string[1]  == 'e':
			for i in world.players:
				listOfPossible.add(i.eid)
		if len(string) > 2: # means that there is a selector
			selectors = string[3:].split(',')
			for i in selectors:
				if i.find('=') == 1:
					k,v = i.split('=')
				else:
					k,v = i,None
				listOfPossible = fiter(lambda x: x.d.get(k) == v,listOfPossible)
		return listOfPossible
	else:
		for i in world.players:
			if world.players.username == string:
				return i