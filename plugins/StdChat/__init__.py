def chat(p,msg):
	prefix = p.f.c.getData(p.display_name).get('prefix') or ""
	pretext = p.f.c.getData(p.display_name).get('pretext') or ""
	suffix = p.f.c.getData(p.display_name).get('suffix') or ""
	message = "{2}{0}{4}:{3}{1}".format(p.display_name, msg,prefix,pretext,suffix)
	p.logger.info(message)  # Write chat message in server console	#print(vars(p.f))
	#print(p.f.send_chat)
	#print('colorcodes')
	#print(p.f.l.colorCodes.to_json(message))
	p.f.dfa('send_packet',('chat_message', p.buff_type.pack_json(p.f.l.colorCodes.colorCodes.to_json(message)) + p.buff_type.pack('b', 0)))
	#p.f.send_chat_json()  # send chat message to all players on server
