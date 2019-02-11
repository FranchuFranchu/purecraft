def player_move(p,x=0,y=0,z=0,xr=0,yr=90,on_ground=None,player=None):
	if p.on_ground:
		p.set_position(x,y,z)
