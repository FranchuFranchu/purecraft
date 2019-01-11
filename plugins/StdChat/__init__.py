def player_chat(p,msg):
	message = "{0}: {1}".format(p.username, msg)
	p.logger.info(message)  # Write chat message in server console
	p.send_chat(message)  # send chat message to all players on server
f={"player_chat":player_chat}
