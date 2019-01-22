import os

def command(p,c):
	print('aa')
	print(c)
	if c.split(' ')[0] == 'rawreload':
		with open('config.yaml') as f:
		    # use safe_load instead load
		    p.f.c = yaml.safe_load(f)
	if c.split(' ')[0] == 'rawreload':
		os.system('python3 ./'+os.path.realpath(__file__)+'/../../../.')
		import sys
		sys.exit(0)