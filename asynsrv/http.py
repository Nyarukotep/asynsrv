import asyncio
__all__ = ['Request']
class Request:
    def __init__(self, addr):
        self.start = {}
        self.header = {}
        self.body = ''
        self.cache = ''
        self.addr = addr

    async def recv(self, loop, conn):

        while self.header.get('Content-Length',1):
            try:
                buffer = await asyncio.wait_for(self.sock_recv(loop, conn),5)
            except asyncio.TimeoutError:
                print(self.addr, 'Connection close due to timeout')
                raise Exception
            if buffer:
                self.parse(buffer)
            else:
                print(self.addr, 'Connection closed by client')
                raise Exception
    async def sock_recv(self, loop, conn):
        data = await loop.sock_recv(conn,1024)
        return data

    def parse(self, buffer):
        self.cache = self.cache + buffer.decode()
        while '\r\n' in self.cache and not self.body:
            line, self.cache = self.cache.split('\r\n', 1)
            if not self.start:
                self.start['method'], self.start['target'], self.start['version'] = line.split()
                if '?' in self.start['target']:
                    self.start['target'], temp = self.start['target'].split('?',1)
                    self.start['query'] = {}
                    args=temp.split('&')
                    for arg in args:
                        k,v=arg.split('=')
                        self.start['query'][k]=v
            elif line:
                k, v = line.split(': ', 1)
                if v.isdigit():
                    self.header[k] = int(v)
                else:
                    self.header[k] = v
            elif not line:
                self.header['Content-Length'] = self.header.get('Content-Length', 0)
                t = self.header['Content-Length']
                self.body = self.cache[:t]
                self.header['Content-Length'] = self.header['Content-Length'] - len(self.cache[:t])
                self.cache = self.cache[t:]
        if self.body:
            t = self.header['Content-Length']
            self.body = self.body + self.cache[:t]
            self.header['Content-Length'] = self.header['Content-Length'] - len(self.cache[:t])
            self.cache = self.cache[t:]

    def __repr__(self):
        return 'Request from ' + str(self.addr)\
            + '\nStart line:\n\t' + '\n\t'.join(['%s:%s' % item for item in self.start.items()])\
            + '\nHeader:\n\t'+'\n\t'.join(['%s:%s' % item for item in self.header.items()])\
            + '\nBody:\n\t'+ repr(self.body)