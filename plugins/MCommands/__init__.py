def command(p,c):
	c = c.split(' ')
	if c[0] in ['gamemode','gm']:
		p.send_gamemode(c[1])
	elif c[0] == 'tp':
		print('TPed')
		p.set_position((int(c[1]),int(c[2]),int(c[3])))
	elif c[0] == 'spawn':
		print('spawned')
		p.send_mob(123,40,90,(0,254,0),0,0,0) # spawn a pig for testing purposes