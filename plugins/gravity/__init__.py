from math import floor
def player_joined(p):
	p.falling_time = 0
def tick(p):
	if p.on_ground or p.flying == False :
		v = (0.98**floor(p.falling_time) - 1) * 3.92
		print(p.falling_time,v)
		p.falling_time+=1
		p.send_packet("entity_velocity",
			p.bt.pack_varint(p.eid)+ # player's eid
			p.pk('hhh',0,int(v*1000),0) 
			)
	else:
		p.falling_time = 0