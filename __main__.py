"""
Example "chat room" server

This server authenticates players, then spawns them in an empty world and does
the bare minimum to keep them in-game. Players can speak to eachother using
chat.

Supports Minecraft 1.11. Earlier versions may not work.
"""
import yaml
from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol
from importlib import import_module as impm
from os import listdir
with open('config.yaml') as f:
    # use safe_load instead load
    config = yaml.safe_load(f)
import plugins as pack
from os import listdir
for i in listdir('./plugins'):
    if i != '__init__.py':
        impm('plugins.{}'.format(i))
class ChatRoomProtocol(ServerProtocol):
    def player_joined(self):
        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)
        self.xr = self.yr = 0
        # Send "Join Game" packet
        self.send_packet("join_game",
            self.buff_type.pack("iBiBB",
                0,                              # entity id
                1,                              # game mode
                0,                              # dimension
                0,                              # max players
                0),                             # unused
            self.buff_type.pack_string("flat"), # level type
            self.buff_type.pack("?", False))    # reduced debug info

        # Send "Player Position and Look" packet

        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                0,                         # x
                255,                       # y
                0,                         # z
                0,                         # yaw
                90,                         # pitch
                0b00000),                  # flags
            self.buff_type.pack_varint(0)) # teleport id
        self.send_empty_chunk(0,0)
        self.send_block_change(0,253,0,2)
        # Start sending "Keep Alive" packets
        self.ticker.add_loop(20, self.update_keep_alive)

        # Announce player joined
        self.factory.send_chat(u"\u00a7e%s has joined." % self.display_name)
        def handle_chat(self, message):
            message = message.encode('utf8')
            self.plugin_event("player_chat", message)
            message = "<{0}> {1}".format(self.username, message)
            self.logger.info(message)  # Write chat message in server console
            self.send_chat(message)  # send chat message to all players on server

    def handle_command(self, command_string):
        self.logger.info("Player " + self.username + " issued server command: " + command_string)
        command_list = command_string.split(" ")  # Command list - e.g ['/login','123123123','123123123']
        command, arguments = command_list[0], command_string.split(" ")[1:]  # Get command and arguments
        self.plugin_event("player_command", command, arguments)
    def packet_player_look(self,buff):
        self.xr,self.yr,_ = buff.unpack('ffb') 
    def packet_player_position(self, buff):
        x, y, z, on_ground = buff.unpack('dddb')  # X Y Z - coordinates, on ground - boolean
        #print(x,y,z,on_ground)
        self.plugin_event("player_move", x, y, z,on_ground)
        #self.position.set(x, y, z)
        # Currently don't work
        '''for eid,player in players.iteritems():
            if player!=self:
                player.send_spawn_player(eid,player.uuid,x,y,z,0,0)
        '''

    def packet_chat_message(self, buff):
        chat_message = buff.unpack_string()
        self.plugin_event("rawchat",chat_message)
        if chat_message[0] == '/':
            #self.handle_command(chat_message[1:])  # Slice to shrink slash
            self.plugin_event("command",chat_message[1:])
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
        position = (x,y,z)
        #print(yr,xr)
        self.send_position_and_look(position, xr, yr, on_ground)

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
    def plugin_event(self,s,*args,**kwargs):
        for i in pack.__all__:
            if i not in '__pycache__init__.py':
                #print(i,s)
                try:
                    exec('pack.{}.f.get("{}")(p,*args,**kwargs)'.format(i,s),{"p":self,"args":args,"kwargs":kwargs,"pack":pack})
                except TypeError:
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
                         self.buff_type.pack_chat(message_bytes) +
                         self.buff_type.pack('b', position)
                         )

    def send_chat_json(self, message_bytes, position=0):  # args: (message[dict], tp[int])
        self.send_packet('chat_message', self.buff_type.pack_json(message_bytes) + self.buff_type.pack('b', position))

    def send_title(self, message, json=False, position=0):  # message, json msg, position: 0 for title, 1 for subtitle
        if json:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_json(message))
        else:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_chat(message))

    def send_keep_alive(self, keepalive_id):  # args: (varint data[int])
        self.send_packet("keep_alive", self.buff_type.pack_varint(keepalive_id))

    def send_plist_head_foot(self, header, footer):  # args: str (header, footer)
        self.send_packet("player_list_header_footer",
                         self.buff_type.pack_chat(header) +
                         self.buff_type.pack_chat(footer))

    def send_block_change(self, x, y, z, block_id):  # args: int (x, y, z, block id)
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


class ChatRoomFactory(ServerFactory):
    protocol = ChatRoomProtocol
    motd = config['motd']
    force_protocol_version = config.get('force_protocol_version')

    def send_chat(self, message):

        for player in self.players:
            player.send_packet("chat_message", player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0))


def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default="", help="address to listen on")
    parser.add_argument("-p", "--port", default=25565, type=int, help="port to listen on")
    args = parser.parse_args(argv)

    # Create factory
    factory = ChatRoomFactory()

    # Listen
    factory.listen(args.host, args.port)
    reactor.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
