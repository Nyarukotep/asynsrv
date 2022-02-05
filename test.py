import asynsrv
def asg(mfc):
    cat={
        1:test,
    }
    mtc = cat.get(1,test)
    return mtc()
def test():
    msg = {'auth': 0,
           'text': 'Hello World',
           'body': '<h1>Hello World</h1>'}
    return msg
s=asynsrv.server()
s.start(asg)