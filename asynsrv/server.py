import asyncio, socket
from .http import httpreq, httprsp
__all__ = ['server']

class server:
    def __init__(self, ip = 'localhost', port = 11456):
        self.ip = ip
        self.port = port
        self.timeout = 5
        self.loop = asyncio.new_event_loop()
        self.ws = {}
    
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
            self.loop.create_task(self.httpconn(conn,addr))

    async def httpconn(self, conn, addr):
        print(addr,'Start connection')
        while True:
            t = self.timeout
            req = httpreq(addr)
            try:
                await req.recv(self.loop, conn) #message from client
            except:
                conn.close()
                return
            print(req)
            rsp = httprsp(self.func(req))
            await rsp.send(self.loop, conn)
            print(addr, 'Complete response')
            if req.header.get('Connection','None') != 'keep-alive':
                print(addr, 'Connection close')
                break
            print(addr, 'Connection reuse')
        conn.close()
        print(addr, 'Connection close')