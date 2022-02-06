import asynsrv
def asg(req, param):
    cat={
        1:test,
    }
    task = cat.get(1,test)
    return task(req, param)
def test(req, param):
    msg = {'auth': 1,
           'text': 'Hello World',
           'body': '<h1>Hello World</h1>'}
    return msg, param
s=asynsrv.server()
s.start(asg)