
def player_move(p,x=0,y=0,z=0,xr=0,yr=90,on_ground=None,player=None):
	#print(p.y-y,p.on_ground)
	if p.on_ground:
		p.set_position(x,y,z)
	else: # if the player is not on ground
		if not p.flying: # and is not flying
				if p.y-y < 0 and p.y-y > -1:  # and before this packet was sent he was 0 to 1 blocks higher
					self.falling_time=p.y-y/0.02	#0.02 seems to be the proportion between the initial height distance and the ticks the player will continue falling
	p.x,p.y,p.z,p.on_ground = (x,y,z,on_ground)
