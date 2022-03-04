import asynsrv
import time
def asg(reqd, param):
    if 'FIN' in reqd:
        if 'Time' in reqd['body']:
            msg = {'WSPUSH':int(reqd['body'].split()[1]), 'body':b'time'}
            return msg, param
        else:
            msg = {'body':reqd['body'].encode()}
            return msg, param
    elif 'WSPUSH' in reqd:
        return {'WSPUSH':1,'PUSHID':1, 'body': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).encode()},param
    else:
        cat={
            '/':hw,
            '/ws':ws,
        }
        task = cat.get(reqd['target'], hw)
        return task(reqd, param)

def ws(reqd, param):
    body=template('ws.html')
    addr = 'ws://'+param['SVRIP'] + ':' + str(param['SVRPORT'])
    body = body.replace('$websocket$', addr)
    print(body)
    msg = {'AUTH': 1,
            'text': 'ws',
            'body': body.encode()}
    return msg, param

def hw(reqd, param):
    msg = {'AUTH': 1,
        'text': 'Hello World',
        'body': b'<h1>Hello World</h1>'}
    if param['WSCONN']:
        wsdict = {}
        for key in param['WSCONN']:
            wsdict[key] = {'body':b'helloworld'}
        msg['WSPUSH'] = wsdict
    return msg, param

def template(filename):
    f=open(filename,'r',encoding='utf-8')
    return f.read()

s=asynsrv.server()
s.start(asg)