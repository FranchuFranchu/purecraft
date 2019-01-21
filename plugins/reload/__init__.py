import os

def command(p,c):
	print('aa')
	print(c)
	if c.split(' ')[0] == 'reload':
		os.system('python3 ./'+os.path.realpath(__file__)+'/../../../.')
		import sys
		sys.exit(0)