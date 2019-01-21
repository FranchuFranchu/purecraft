def command(p,c):
	c = c.split(' ')
	if c[0] in ['gamemode','gm']:
		p.send_gamemode(c[1])
	elif c[0] == 'tp':
		print('TPed')
		p.set_position((int(c[1]),int(c[2]),int(c[3])))