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
        self.ws = {} #{addr: conn}
    
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
        self.debug(str(addr) + 'Start connection')
        while True:
            req = httpreq(addr)
            try:
                await req.recv(self.loop, conn) #message from client
            except:
                conn.close()
                return
            print(req)
            msg, self.param = self.func(req.data, self.param)
            wspush = msg.pop('WSPUSH',0)
            rsp = httprsp(msg, req.data)
            await rsp.send(self.loop, conn)
            if wspush:
                for key in wspush:
                    if self.param['ws'].get(key, 0):
                        print('key:',key)
                        print('wspushkey', wspush[key])
                        wsrsp = wssend(self.loop, {}, wspush[key])
                        await wsrsp.send(self.param['ws'][key])
            self.debug(str(addr) + 'Complete response')
            if rsp.data.get('Upgrade','None') == 'websocket':
                self.loop.create_task(self.wsconn(conn, addr, msg))
                self.debug(str(addr) + 'Start websocket connection')
                return
            elif rsp.data.get('Connection','None') != 'keep-alive':
                self.debug(str(addr) + 'Connection close')
                break
            self.debug(str(addr) + 'Connection reuse')
        conn.close()
        self.debug(str(addr) + 'Connection close')
    
    async def wsconn(self, conn, addr, msg):
        self.debug(str(addr) + 'Start websocket connection')
        self.param['ws'][addr] = conn
        print('ws:', self.param['ws'])
        while True:
            wsreq = wsrecv(self.loop)
            try:
                await wsreq.recv(conn) #message from client
            except:
                conn.close()
                break
            print(wsreq)
            if wsreq.data['opcode'] == 9:
                wsrsp = wssend(self.loop, wsreq.data, {})
                await wsrsp.send(conn)
            else:
                msg, self.param = self.func(wsreq.data, self.param)
                if 'PUSH' in msg:
                    self.loop.create_task(self.wsph(conn,addr,msg))
                    print('start wsph')
                else:
                    wsrsp = wssend(self.loop, wsreq.data, msg)
                    await wsrsp.send(conn)
            if not msg:
                conn.close()
                break
            print(addr, 'Complete response')
        print(addr, 'websocket close')
        self.param['ws'].pop(addr)
        

    async def wsph(self, conn, addr, msg):
        while 'PUSH' in msg and addr in self.param['ws']:
            msg, self.param = self.func(msg, self.param)
            wsrsp = wssend(self.loop, {}, msg)
            await wsrsp.send(conn)
            await asyncio.sleep(msg.get('PUSH',0))
        print('end ws push')
    
    def debug(self, c):
        if self.param.get('DEBUG', 1):
            print(c)