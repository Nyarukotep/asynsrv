import asynsrv
import time
def asg(reqd, param):
    if 'FIN' in reqd:
        cat={
            'start time':stime,
            'time':sstime,
            'close':close
        }
        task = cat.get(reqd['body'], echo)
        return task(reqd, param)
    elif 'PUSHID' in reqd:
        return sstime(reqd, param)
    else:
        cat={
            '/': hello,
        }
        task = cat.get(reqd['target'], eee)
        return task(reqd, param)
def eee(reqd, param):
    msg = {'AUTH': 1,
            'text': 'Hello World',
            'body': '<h1>Hello World</h1>'}
    return msg, param

def stime(reqd, param):
    msg = {'PUSH':5, 'PUSHID':1, 'body':'time'}
    return msg, param

def echo(reqd, param):
    msg = {'body':reqd['body']}
    return msg, param

def hello(reqd, param):
    msg = {'AUTH': 1,
            'text': 'Hello World',
            'body': '<h1>Hello World</h1>'}
    if param['WS']:
        w = {}
        wsmsg = param['WS']
        for key in wsmsg:
            w[key] = {'body':'helloworld'}
        msg['WSPUSH'] = w
    return msg, param

def close(reqd, param):
    return {}, param

def sstime(reqd, param):
    return {'PUSH':5,'PUSHID':1, 'body': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())},param

s=asynsrv.server()
s.start(asg)