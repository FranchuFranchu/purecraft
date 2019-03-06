from data import *
from twisted.internet import reactor
import re
def getKey(d,k): # get value from a dictionary, if KeyError then return the key
	try:
		return d[k]
	except KeyError:
		return k
commandSystem = {}
def newNode(type_,f=None,name=None,exec_=True):
	node = {}
	node['type'] = type_
	node['name'] = name
	node['children'] = []
	node['executable'] = exec_
	node['suggestion'] = True
	node['redirect'] = False
	node['parser'] = 'brigadier:string'
	node['f'] = f
	node['properties'] = {'behaviour':1}
	return node
commandGraph = newNode(0)
def addChild(node,child):
	node['children'].append(child)
	return node
class commandFunction:
	def __init__(self,func,fmt,perm='',help_=''):
		self.factory = None
		self.perm = perm
		self.help = help_
		self.fmt = fmt
		self.mfmt = []
		#print(fmt)
		#print(re.split(r"\s+(?=[^()]*(?:(\(|\<|\[|\{)|$))", fmt))
		for i in re.split(r"\s+(?=[^()]*(?:(\(|\<|\[|\{)|$))", fmt):
			if i == None:
				continue
			if i.startswith('<') and i.endswith('>'):
				self.mfmt.append(('<',i[0:]))
			elif i.startswith('(') and i.endswith(')'):
				self.mfmt.append(('(',i[0:]))
			elif i.startswith('[') and i.endswith(']'):
				self.mfmt.append(('[',i[0:]))
			else:
				self.mfmt.append(('',i[0:]))
		self.func = func
	def __call__(self,player,s):
		if not self.factory:
			self.factory = player.factory
		d = {}
		reg = re.split(r"\s+(?=[^()]*(?:(\(|\<|\[|\{)|$))",s)
		 
		
		lre = 0
		nreg = []
		for i in reg:
			if i != None:
				nreg.append(i)
		reg = nreg
		for i,j in zip(self.mfmt,reg):
			if i[0] == '<':
				d[i[1][1:-1]] = j
				lre+=1
		if lre < len(list(filter(lambda x: x[0] == '<',self.mfmt))):
			player.send_chat('§cCommand §b%s§c expects §b%s§c mandatory arguments, got §b%s§c' % (' '.join([i[1] for i in filter(lambda x: x[0] == '' ,self.mfmt)]), len(list(filter(lambda x: x[0] == '<',self.mfmt))),lre))
			return
		self.func(player,**d)

def commandDecorator(fmt,perm = '',help_ = ''):
	def wrapper(f):
		# make it a command
		m = commandFunction(f,fmt,perm,help_)
		#print(' '.join(list(filter(lambda x: x[0] == '' ,m.mfmt)))
		l = [i[1] for i in filter(lambda x: x[0] == '' ,m.mfmt) # list of constant arguments in m.mfmt, joined by spaces
			]
		pl = l.copy()
		node = commandGraph
		for i in l:
			if newNode(1,name=i,f=f) in node['children'] != None:
				node = node['children'][node['children'].index(newNode(1,name=i,f=f))]
			else:
				node['children'].append(newNode(1,name=i,f=f))
				node = node['children'][node['children'].index(newNode(1,name=i,f=f))]
		l = [i[1][1:-1] for i in filter(lambda x: x[0] == '<' ,m.mfmt) # list of constant arguments in m.mfmt, joined by spaces
			]
		for i in l:
			if newNode(2,name=i,f=f) in node['children'] != None:
				node = node['children'][node['children'].index(newNode(2,name=i,f=f))]
			else:
				node['children'].append(newNode(2,name=i,f=f))
				node = node['children'][node['children'].index(newNode(2,name=i,f=f))]
		commandSystem[' '.join(pl)] = m
		print(commandSystem) 
	return wrapper



class Config():
	def __init__(self,config):
		self.r = config # raw config
		#print('Config.yaml: ',self.r)
		if not self.r.get('groups'):
			self.r['groups'] = {}
	def isIn(self,group,player):
		if not self.r['groups'].get(group):
			return None, "group does not exist"
		elif player not in self.r['groups'][group]['u']:
			return False, "player is not in group"
		else:
			return True, "player is in group"
	def listGroups(self,player):
		# TODO: add inherited groups
		groups = []
		for k,v in self.r['groups'].items():
			if player in v['u']:
				groups.append(k)
		return groups
	def listPermissions(self,player):
		groups = self.listGroups(player)
		perms = []
		for i in groups:
			i = self.r['groups'][i]
			for j in i['p']:
				perms.append(j)
		return perms
	def getData(self,player):
		groups = self.listGroups(player)
		data = {}
		for i in groups:
			i = self.r['groups'][i]
			if i.get('d'):
				data = {**data,**i['d']}
		return data

	def hasPermission(self,player,perm):
		perm = perm.split('.')

		if type(player) != str:
			uname = player.username_
			prot = player
			player = uname
		for i in self.listPermissions(player):
			i = i.split('.')
			matches = True
			for j,k in zip(i,perm):
				if j == '*':
					pass
				elif j != k:
					matches = False
					break
			if matches:
				return True
		return False

class Entity():
	isEntity = True
	def __init__(self,typ,pos=(0,0,0),metadata={},protocol=None):
		self.s = {'x':pos[0],'y':pos[0],'z':pos[0]}
		self.type = typ
		self.pos = pos
		self.protocol = protocol
	def __str__(self):
		return '{0} at {1},{2},{3}'.format(self.type,*self.pos)

class World():
	def __init__(self,players=[],typ=0 ): #type = -1 :nether 0:overworld 1:end;  
		#print(reactor.factory)
		self.type = typ
		self.players = []
		self.chunks = {(0,0):{(0,100,0,1),(2,100,0,2),(4,101,1,3)}}
		self.spawn = (0,101,0)
		self.entities = {}
		self.add_players(*players)
		
		


	def add_players(self,*players):
		for player in players:	
			# set eid (Entity ID)
			player.eid = len(self.entities.keys())
			self.entities[player.eid] = Entity('minecraft:player',pos=self.spawn,protocol=player)


			player.world = self
			player.dfaw = self.do_for_all_world
			self.players.append(player)
	def post_play_add(self,*players): # do this after "Play" packet is sent
		for player in players:	
			# set position
			player.set_position(*self.spawn)

			chunkx = self.spawn[0]//16
			chunkz = self.spawn[2]//16
			player.seeableChunks = []
			for i in range(-0,1):
				for j in range(-0,1):
					player.seeableChunks.append((i+chunkx,j+chunkz))
					player.send_empty_chunk(i+chunkx,j+chunkz)
					try:
						for k in iter(self.chunks[(i+chunkx,j+chunkz)]):
							player.send_block_change(*k)
					except KeyError:
						pass
			for j,i in self.entities.items():
				player.send_mob(j,type_=entities_ids[i.type],pos=i.pos)
	def do_for_all_world(self,fname,*args,target_players=None): # do for all players in the world
		for player in self.players:
			exec('p.{}(*args)'.format(fname),{'args':args,'p':player})



