from .http import *
import asyncio, socket
#from .websocket import *
def id(i,addr):
    cat={
        0:Request,
    }
    msg = cat.get(i,Request)
    return msg(addr)

class server:
    def __init__(self, ip = 'localhost', port = 11456):
        self.ip = ip
        self.port = port
        self.timeout = 5
        self.loop = asyncio.new_event_loop()
    
    def start(self, func):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server.bind((self.ip, self.port))
                break
            except OSError:
                self.port = self.port+1
        self.server.listen()
        self.server.setblocking(False)
        self.func = func
        print('Start server at %s:%d' %(self.ip, self.port))
        self.loop.run_until_complete(self.listen())
    
    async def listen(self):
        while True:
            conn, addr = await self.loop.sock_accept(self.server)
            self.loop.create_task(self.connection(conn,addr))
    
    async def connection(self, conn, addr):
        print(addr,'Start connection')
        tag = 0
        #tag, 0: standard; 1: websocket
        while True:
            t = self.timeout
            req = id(tag,addr)
            try:
                await req.recv(self.loop, conn) #message from client
            except:
                conn.close()
                return
            print(req)
            rsp = self.func(req)
            await self.loop.sock_sendall(conn, rsp)
            print(addr, 'Complete response')
            if req.header.get('Connection','None') != 'keep-alive':
                print(addr, 'Connection close')
                break
            print(addr, 'Connection reuse')
        conn.close()
        print(addr, 'Connection close')