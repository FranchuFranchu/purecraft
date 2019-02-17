from data import *
def getKey(d,k): # get value from a dictionary, if KeyError then return the key
	try:
		return d[k]
	except KeyError:
		return k
class Config():
	def __init__(self,config):
		self.r = config # raw config
		print('Config.yaml: ',self.r)
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
	def __init__(self,typ,pos=(0,0,0),metadata={},protocol=None):
		self.type = typ
		self.pos = pos
		self.protocol = protocol

class World():
	def __init__(self,players=[],typ=0 ): #type = -1 :nether 0:overworld 1:end;  
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
			for i in range(-3,3):
				for j in range(-3,3):
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



