import classes
@classes.commandDecorator('ping','pc.cmd.ping','Pings the server')
def some_func(p,s):
	p.send_chat('Pong!')
