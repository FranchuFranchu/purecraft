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