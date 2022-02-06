import asyncio, socket
from .http import httpreq, httprsp
from .websocket import wsrecv, wssend
__all__ = ['server']

class server:
    def __init__(self, ip = 'localhost', port = 11456):
        self.ip = ip
        self.port = port
        self.timeout = 5
        self.loop = asyncio.new_event_loop()
        self.ws = {}
    
    def start(self, func, param = {}):
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
        self.param = param
        self.param['serverip'] = self.ip
        self.param['serverport'] = self.port
        self.param['ws'] = {}
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
            msg, self.param = self.func(req, self.param)
            rsp = httprsp(req, msg)
            await rsp.send(self.loop, conn)
            
            print(addr, 'Complete response')
            if req.header.get('Connection','None') != 'keep-alive':
                print(addr, 'Connection close')
                break
            print(addr, 'Connection reuse')
        if rsp.msg.get('Upgrade','None') == 'websocket':
            self.loop.create_task(self.wsconn(conn,addr))
            print(addr, 'Start websocket connection')
        else:
            conn.close()
            print(addr, 'Connection close')
    
    async def wsconn(self, conn, addr):
        print(addr,'Start websocket connection')
        self.ws[addr] = conn
        #if 1:
            #self.loop.create_task(self.wspolling(conn,addr,30))
        while True:
            wsreq = wsrecv(self.loop)
            try:
                await wsreq.recv(conn) #message from client
            except:
                conn.close()
                break
            print(wsreq)
            #msg = self.func(wsreq, self.param)
            msg = {}
            wsrsp = wssend(self.loop, wsreq.data, msg)
            await wsrsp.send(conn)
            print(addr, 'Complete response')
        print(addr, 'websocket close')
        self.ws.pop(addr)
        

    async def wspolling(self, conn, addr, time):
        a=1
