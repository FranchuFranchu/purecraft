def chat(p,msg):
	message = "{0}: {1}".format(p.display_name, msg)
	p.logger.info(message)  # Write chat message in server console	#print(vars(p.f))
	#print(p.f.send_chat)
	#print('colorcodes')
	#print(p.f.l.colorCodes.to_json(message))
	for p in p.f.players:
		print('p')
		p.send_packet('chat_message', p.buff_type.pack_json(p.f.l.colorCodes.colorCodes.to_json(message)) + p.buff_type.pack('b', 0))
	#p.f.send_chat_json()  # send chat message to all players on server
