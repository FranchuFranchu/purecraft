JUMP_TIME = 0.5 # jump length in seconds

JUMP_TIME *= -1000
JUMP_TIME /= 50

def player_move(p,x=0,y=0,z=0,xr=None,yr=None,on_ground=None,player=None):
	#print(p.y-y,p.on_ground)
	if xr != None:
		p.xr,p.yr = xr,yr
	if on_ground:
		p.set_position(x,y,z)
	else: # if the player is not on ground
		if not p.flying: # and is not flying
			if p.y-y < 0 and p.y-y > -1 and p.prev_on_ground:  # and before this packet was sent he was 0 to 1 blocks higher
				p.falling_time = int(JUMP_TIME)
				#p.falling_time=(p.y-y/0.02)+4969	#0.02 seems to be the proportion between the initial height distance and the ticks the player will continue falling
				#print(p.falling_time)
	p.prev_x,p.prev_y,p.prev_z,p.prev_on_ground = (p.x,p.y,p.z,p.on_ground)
	p.x,p.y,p.z,p.on_ground = (x,y,z,on_ground)