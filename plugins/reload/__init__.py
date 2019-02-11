import os

def command(p,c):
	c = c.split(' ')
	print(c)
	if not p.f.c.hasPermission(p.username,'purecraft.reload'):
		p.send_chat('Insufficient Permsissions')
		print('das')
		return 
	if c[0] == 'rawreload':
		with open('config.yaml') as f:
			# use safe_load instead load
			p.f.c = yaml.safe_load(f)
	if c[0] == 'rawreload':
		os.system('python3 ./'+os.path.realpath(__file__)+'/../../../.')
		import sys
		sys.exit(0)
	elif c[0] == 'reload':
		p.f.pack = __import__('plugins')
		for i in os.listdir('./lib'):
			if i != '__init__.py':
				lib = __import__('lib.{}'.format(i))
		p.f.l = lib
		
		p.send_chat('Insufficient Permsissions',2)