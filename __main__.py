"""
Purecraft 1.0
supports < 1.12
by copying this program, you agree to sell your program to me haha no jk
"""
import traceback as tb
from classes import Config,World
from twisted.internet import task
from quarry.types.uuid import UUID
import yaml
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol
from importlib import import_module as impm
from os import listdir
curdir = __file__.split('__main__')[0]
with open(curdir+'config.yaml') as f:
    # use safe_load instead load
    config = yaml.safe_load(f)
import plugins as pack
from os import listdir


class Obj:
    def __init__(self):
        pass
    #def __setattr__(self,attr,val):
    #   exec('self.{} = val'.format(attr),{'self':self,'val':val})
for i in listdir(curdir+'plugins'):
    if i != '__init__.py':
        impm('plugins.{}'.format(i))
class PurecraftProtocol(ServerProtocol):
    def packet_steer_vehicle(self,buff):
        buff.discard()
        print('steer vehicle')
    def packet_status_request(self, buff):
        protocol_version = self.factory.force_protocol_version
        if protocol_version is None:
            protocol_version = self.protocol_version

        d = {
            "description": {
                "text":     self.factory.motd
            },
            "players": {
                "online":   len(self.factory.players),
                "max":      self.factory.max_players
            },
            "version": {
                "name":    "Purecraft < 1.12.2", #self.factory.minecraft_versions.get(protocol_version,"???"),
                "protocol": protocol_version
            }
        }
        print(self.factory.minecraft_versions.get(
                                protocol_version,
                                "???"),)
        if self.factory.favicon is not None:
            with open(curdir+self.factory.favicon, "r") as fd:
                print()
                x = fd.read()
                print(len(x))
                d = {**d,**eval('{"favicon":"data:image/png;base64,{data"}'.replace('{data',x).replace('\n', ''))}
                
        # send status response
        self.send_packet("status_response", self.buff_type.pack_json(d))

    def player_joined(self):
        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)
        self.isProtocol = True
        self.logger.setLevel(self.factory.level)
        self.username_ = self.display_name
        self.bt = self.buff_type
        self.pk = self.buff_type.pack
        self.send_chat('hi')
        self.xr = self.yr = 0   
        self.on_ground = False
        self.factory.w[0].add_players(self)
        # Send "Join Game" packet
        self.send_packet("join_game",
            self.buff_type.pack("iBiBB",
                self.eid,                              # entity id
                1,                              # game mode
                0,                              # dimension
                0,                              # max players
                0),                             # unused
            self.buff_type.pack_string("flat"), # level type
            self.buff_type.pack("?", False))    # reduced debug info

        # Send "Player Position and Look" packet
        self.position = (0,255,0)
        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                0,                         # x
                101,                       # y
                0,                         # z
                0,                         # yaw
                90,                         # pitch
                0b00000),                  # flags
            self.buff_type.pack_varint(0)) # teleport id

        self.plugin_event('pre_player_joined') # tell plugins that the player joined
        # start ticking 
        loop = task.LoopingCall(self.plugin_event,'tick')
        loopDeferred = loop.start(0.05)
        # set world
        # send 7x7 chunks  around the player
        for i in range(-3,3):
            for j in range(-3,3):
                self.send_empty_chunk(i,j)

        # make a small parkour
        self.x,self.y,self.z = (0,101,0)
        #self.send_packet('entity',self.bt.pack_varint(123))
        #self.send_mob(123,40,90,(0,101,0),0,0,0) # spawn a pig for testing purposes
        print("Player %s has the following permissions: "%self.display_name,*self.factory.c.listPermissions(self.display_name))
        # Start sending "Keep Alive" packets
        self.ticker.add_loop(20, self.update_keep_alive)
        self.f = self.factory
        self.inv = {}
        self.flying = False
        self.world.post_play_add(self)
        self.plugin_event('player_joined')
        # Announce player joined
        #print(self.f.c.hasPermission(self.display_name,'sdfsdsd'))
        self.factory.send_chat(u"\u00a7e%s has joined." % self.display_name)
        

    def packet_player_look(self,buff):
        self.xr,self.yr,on_ground = buff.unpack('ffb') 
    def packet_player_position(self, buff):
        #self.pon_ground = True
        x, y, z, on_ground = buff.unpack('dddb')  # X Y Z - coordinates, on ground - boolean
        


        #print(x,y,z,on_ground)
        self.plugin_event("player_move", x, y, z, on_ground=on_ground)

        #self.position.set(x, y, z)
        # Currently don't work
        '''for eid,player in players.iteritems():
            if player!=self:
                player.send_spawn_player(eid,player.uuid,x,y,z,0,0)
        '''
    def packet_creative_inventory_action(self,buff):
        place = buff.unpack('h')
        slot = buff.unpack_slot()
        self.inv[place] = slot
        self.plugin_event('creative_inventory_action',place,slot)
    def packet_player_block_placement(self,buff):
        x,y,z = buff.unpack_position()
        face = buff.unpack_varint() 
        using_main_hand = buff.unpack_varint() == 0
        crx,cry,crz = buff.unpack('fff')
        self.plugin_event('r_block_placed',x,y,z,face,using_main_hand,crx,cry,crz)
        neg = 1
        i = face
        if i%2 == 0:
            neg = -1
        if i < 2:
            y = y + neg
        elif i < 4:
            z = z + neg
        elif i < 6:
            x = x + neg
        if self.inv.get(36) not in (None,{}):
            self.f.dfa('send_block_change',(x,y,z,self.inv[36]['item']))

    def packet_player_position_and_look(self, buff): # not working
        x, y, z,xr,yr, on_ground = buff.unpack('dddffb')  # X Y Z - coordinates, on ground - boolean
        #print(x,y,z,on_ground)
        #print(x,y,z,self.xr,self.yr) 
        self.plugin_event("player_move", x, y, z,xr,yr,on_ground=on_ground)
    def packet_chat_message(self, buff):
        chat_message = buff.unpack_string()
        print('[CHAT]',chat_message)
        self.plugin_event("rawchat",chat_message)
        if chat_message[0] == '/':
            #self.handle_command(chat_message[1:])  # Slice to shrink slash
            try:
                self.plugin_event("command",chat_message[1:])
            except Exception as e:
                self.logger.log(4,'{} made a command, raising an error:'.format(self.username_))
                self.logger.log(4,repr(e))
                self.send_chat(tb.format_exc())

        else:
            #self.handle_chat(chat_message)
            self.plugin_event("chat",chat_message)

    '''def send_spawn_player(self,entity_id,player_uuid,x,y,z,yaw,pitch):
        buff = self.buff_type.pack_varint(entity_id)+self.buff_type.pack_uuid(player_uuid)+self.buff_type.pack("dddbbBdb",x,y,z,yaw,pitch,0,7,health)
        self.send_packet("spawn_player",buff)
    '''

    def send_empty_chunk(self, x, z):  # args: chunk position ints (x, z)
        self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))

    def send_change_game_state(self, reason, state):  # http://wiki.vg/Protocol#Change_Game_State
        self.send_packet("change_game_state", self.buff_type.pack('Bf', reason, state))

    def set_position(self, x, y, z, xr=None, yr=None, on_ground=False):
        if xr == None:
            xr = self.xr
        if yr == None:
            yr = self.yr
        self.position = position = (x,y,z)
        #print(yr,xr)
        self.dfaw('send_position_and_look',position, xr, yr, on_ground)

    def send_position_and_look(self, position, xr, yr,
                               on_ground):  # args: num (x, y, z, x rotation, y rotation, on-ground[bool])
        x, y, z = position
        #print(position)
        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                x,                         # x
                y,                       # y
                z,                         # z
                xr,                         # yaw
                yr,                         # pitch
                0b00000),                  # flags
            self.buff_type.pack_varint(0)) # teleport id
    def send_gamemode(self,gm):
        self.send_packet('change_game_state',self.pk('Bf',3,float(gm)))
    def send_abilities(self, flying, fly, god, creative, fly_speed,
                       walk_speed):  # args: bool (if flying, if can fly, if no damage, if creative, (num) fly speed, walk speed)
        bitmask = 0
        if flying: bitmask = bitmask | 0x02
        if fly: bitmask = bitmask | 0x04
        if god: bitmask = bitmask | 0x08
        if creative: bitmask = bitmask | 0x01
        self.send_packet("player_abilities", self.buff_type.pack('bff', bitmask, float(fly_speed), float(walk_speed)))

    def send_spawn_pos(self, position):  # args: (x, y, z) int
        self.send_packet("spawn_position",
                         self.buff_type.pack('q', position.get_pos())  # get_pos() is long long type
                         )
    def packet_player_abilities(self,buff):
        b = buff.unpack('b')
        buff.discard()
        ab = list((b >> i) & 0x1 for i in range(0,4))
        print(b,*ab)

        self.flying = ab[1] == 1
    def plugin_event(self,s,*args,**kwargs):
        for i in self.factory.pack.__all__:
            if i not in '__pycache__init__.py':
                #print(i,s)
                try:
                    if s != 'tick': 
                        pass#print(s,i)
                    exec('pack.{}.{}(p,*args,**kwargs)'.format(i,s),{"pack":self.factory.pack,"args":args,"kwargs":kwargs,"p":self})
                except AttributeError:
                    if s != 'tick':
                        pass#print(s,i)
                    pass

    def send_game(self, entity_id, gamemode, dimension, difficulty, level_type,
                  dbg):  # args: int (entity id, gamemode, dimension, difficulty, max players, level type[str], reduced debug info[bool])
        max_players = 25  # This is no longer used in Minecraft protocol
        self.send_packet("join_game",
                         self.buff_type.pack('iBbBB',
                                             entity_id, gamemode, dimension, difficulty,
                                             max_players) + self.buff_type.pack_string(level_type) +
                         self.buff_type.pack('?', dbg)
                         )

    def send_chat_all(self, message_bytes, position=0):  # Send chat message for all players
        for player in players.values():
            player.send_packet('chat_message',
                               player.buff_type.pack_chat(message_bytes) +
                               player.buff_type.pack('b', position)
                               )

    def send_chat(self, message_bytes, position=0):  # args: (message[str], position[int])
        self.send_packet('chat_message',
                         self.buff_type.pack_json([message_bytes]) +  
                         self.buff_type.pack('B', position)
                         )
        print(message_bytes)

    def send_chat_json(self, message_bytes, position=0):  # args: (message[dict], tp[int])
        self.send_packet('chat_message', self.buff_type.pack_json(message_bytes) + self.buff_type.pack('b', position))

    def send_title(self, message, json=False, position=0):  # message, json msg, position: 0 for title, 1 for subtitle
        if json:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_json(message))
        else:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_chat(message))
    def send_mob(self,eid,type_,pos=(0,0,0),yaw=0,pitch=0,headpitch=0,uuid=UUID.random()):
        self.send_packet('spawn_mob', 
            self.bt.pack_varint(eid)+
            self.bt.pack_uuid(uuid)+
            self.bt.pack_varint(type_)+
            self.bt.pack('dddfffhhh',*pos,yaw,pitch,headpitch,0,0,0)+
            self.bt.pack_entity_metadata({}))
    def send_keep_alive(self, keepalive_id):  # args: (varint data[int])
        self.send_packet("keep_alive", self.buff_type.pack_varint(keepalive_id))
        
    def send_plist_head_foot(self, header, footer):  # args: str (header, footer)
        self.send_packet("player_list_header_footer",
                         self.buff_type.pack_chat(header) +
                         self.buff_type.pack_chat(footer))

    def send_block_change(self, x, y, z, block_id):  # args: int (x, y, z, block id)
        print(block_id<<4)
        self.send_packet("block_change", self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (
            z & 0x3FFFFFF)) + self.buff_type.pack_varint((block_id << 4) | 0))
    def player_left(self):
        ServerProtocol.player_left(self)

        # Announce player left
        self.factory.send_chat(u"\u00a7e%s has left." % self.display_name)

    def update_keep_alive(self):
        # Send a "Keep Alive" packet

        # 1.7.x
        if self.protocol_version <= 338:
            payload =  self.buff_type.pack_varint(0)

        # 1.12.2
        else:
            payload = self.buff_type.pack('Q', 0)
        
        self.send_packet("keep_alive", payload)
        #if not self.on_ground:
        #    self.send_position_and_look((self.position[0],self.position[1]-1,self.position[2]),self.xr,self.yr,self.on_ground)

class PurecraftFactory(ServerFactory):
    protocol = PurecraftProtocol
    favicon = 'favicon_base64.txt'
    motd = config['motd']
    force_protocol_version = config.get('force_protocol_version')
    def __init__(self):
        ServerFactory.__init__(self)
        self.pack = pack
        self.l = Obj()
        self.c = Config(config)
        self.dfa = self.do_for_all
        self.worlds = [World()]
        self.w = self.worlds
        lib = __import__('lib')
        for i in listdir(curdir+'lib'):
            tmp = __import__('lib.{}'.format(i),lib)
            exec('self.l.{} = tmp'.format(i),{'self':self,'tmp':tmp})

    def send_chat_json(self, message_bytes, position=0):
        for p in self.players:
            p.send_packet('chat_message', p.buff_type.pack_json(message_bytes) + self.buff_type.pack('b', position))
    def send_chat(self, message):

        for player in self.players:
            player.send_packet("chat_message", player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0))
    def get_player(self,username):
        for player in self.players:
            if player.username == username:
                return player
    def do_for_all(self,fname,args,target_players=None):
        for player in self.players:
            exec('p.{}(*args)'.format(fname),{'args':args,'p':player})


def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default="", help="address to listen on")
    parser.add_argument("-p", "--port", default=25565, type=int, help="port to listen on")
    parser.add_argument("-d", "--debug", default=5, type=int, help="debug level, lower is verboser")
    args = parser.parse_args(argv)

    # Create factory
    factory = PurecraftFactory()
    factory.level = args.debug
    # Listen
    factory.listen(args.host, args.port)
    reactor.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

