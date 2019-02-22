from copy import copy
def command(player, command):
	args = command.split(' ') # getting arguments
	command = args[0] # getting command
	args.remove(args[0])
	print(command)
	if command == 'matchesselector':
		print('assdgf')
		player.logger.log(4,'sss')
		# copy everything since selectorParser is a read-only lib
		m = copy(player.f.l.selectorParser.selectorParser.parse(
			args[0],
			copy(copy(player.world).entities[player.eid]),
			copy(player.world)))
		m = [m] if type(m) != list else m
		print(m)
		for i in m: # list entities matching the selector
			player.send_chat(str(i))
	if command == 'gamemode' or command == 'gm':
		# checking if no arguments
		if args == []: return # it needs to send a message to sender about error
		
		mode = '1' if args[0] == 'creative' else '0' if args[0] == 'survival' else args[0] # getting mode if player use /gamemode creative or /gm creative
		player.send_gamemode(mode) # setting gamemode for sender
	elif command == 'tp':
		# checking if no arguments
		if args == []: return

		x, y, z = int(args[0]), int(args[1]), int(args[2]) # getting target position
		player.set_position(x, y, z) # setting player position
	elif command == 'spawn':
		player.send_mob(123, 40, 90, (0, 254, 0), 0, 0, 0)
	elif command == 'kick':
		print(command)	
		if player.command.hasPermission(player.username,'mc.kick'):
			player.send_chat('You have no permission to run that command')
			k = player.f.get_player(args[0])

			if k == None:
				player.send_chat('Player %s not found' % (args[0]))
			else:
				player.send_chat('Player %s has been kicked: %s' % (args[0],args[1]))
		else:
			player.send_chat('You have no permission to run that command')
		player.send_chat('You have no permission to run that command')

