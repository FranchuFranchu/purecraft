<<<<<<< HEAD
def command(p,c):
	c = c.split(' ')
	if c[0] in ['gamemode','gm']:
		p.send_gamemode(c[1])
	elif c[0] == 'tp':
		print('TPed')
		p.set_position((int(c[1]),int(c[2]),int(c[3])))
	elif c[0] == 'spawn':
		print('spawned')
		p.send_mob(123,40,int(c[1]),(0,254,0),0,0,0) # spawn a pig for testing purposes
	elif c[0] == 'kick':
		print(c)	
		if p.c.hasPermission(p.username,'mc.kick'):
			p.send_chat('You have no permission to run that command')
			k = p.f.get_player(c[1])

			if k == None:
				p.send_chat('Player %s not found' % (c[1]))
			else:
				p.send_chat('Player %s has been kicked: %s' % (c[1],c[2]))
		else:
			p.send_chat('You have no permission to run that command')
		p.send_chat('You have no permission to run that command')
=======
def command(player, command):
	args = command.split(' ') # getting arguments
	command = args[0] # getting command
	args.remove(args[0])

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
>>>>>>> 4cc6fe620a9cdeb564938fee50b756f9e51475d8
