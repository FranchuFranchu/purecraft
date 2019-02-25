from copy import copy
from classes import commandDecorator
def command(player, command):
	args = command.split(' ') # getting arguments
	command = args[0] # getting command
	args.remove(args[0])
	print(command)

	if command == 'spawn':
		player.send_mob(123, 40, 90, (0, 254, 0), 0, 0, 0)
	elif command == 'kick':
		print(command)	
		if player.command.hasPermission(player.username,'mc.kick'):
			player.send_chat('You have no permission to run that command')
			k = player.f.get_player(args[0])

			if k == None:
				player.send_chat('Player %s not found' % (args[0]))
			else:
				player.send_chat('Player %s has been kicked: %s' % (args[0],args[1]))
		else:
			player.send_chat('You have no permission to run that command')
		player.send_chat('You have no permission to run that command')

@commandDecorator('matchesselector <selector>','mc.cmd.selector','Lists entities matching a selector')
def matchesSelector(player,selector):
	m = copy(player.f.l.selectorParser.selectorParser.parse(
		selector,
		copy(copy(player.world).entities[player.eid]),
		copy(player.world)))
	m = [m] if type(m) != list else m
	print(m)
	for i in m: # list entities matching the selector
		player.send_chat(str(i))
@commandDecorator('gamemode <gamemode>','mc.cmd.gm','Switches gamemode')
def matchesSelector(player,gamemode):	
	mode = '1' if gamemode == 'creative' else '0' if gamemode == 'survival' else gamemode # getting mode if player use /gamemode creative or /gm creative
	player.send_gamemode(mode) # setting gamemode for sender

@commandDecorator('spawn <eid> <entity_type> <x> <y> <z>','mc.cmd.spawn','Spawns an entity')
def spawn(player, eid, entity_type, x, y, z):
	player.send_mob(int(eid), int(entity_type), (int(x), int(y), int(z)), 0, 0, 0)

@commandDecorator('tp <x> <y> <z>','mc.cmd.tp','Teleports to a position')
def tp(player, x, y, z):
	x, y, z = int(x), int(y), int(z) # getting target position
	player.set_position(x, y, z) # setting player position

@commandDecorator('help','','Shows this message')
def help(player):
	pass