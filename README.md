# Asynsrv
Asynchronous web server framework work with sockets directly, supporting HTTP and WebSocket protocol.

Asynsrv is an asyncio-based asynchronous web server framework developed entirely using the python standard library with no dependencies. asynsrv currently supports both HTTP and WebSocket protocols, allowing for simpler code to control all the details of a web request. It was originally developed to support the Kancolle server emulation project for highly customizable response messages and integration of HTTP and WebSocket protocols.
# Features
- Simple code, easy to modify and deploy, suitable for lightweight tasks
- Supports highly customizable responses for HTTP and WebSocket
- Friendly data format, completely using dictionary as data transfer method
- Full use of asynchronous programming, maintaining multiple connections through a single thread
# Usage
## Start server
Server can be started with the following code
```python
def fun(req, dict)
    ... ...
    return msg, dict
s=asynsrv.server('localhost', 11456)
s.start(fun, dict)
```
- `asynsrv.server`: Used to initialize the server, including specifying the listening port and creating a new asynchronous event loop   
- `asynsrv.start(fun, dict)`: Used to start accepting connections, accept a function parameter `fun` and an optional dictionary parameter `dict`, defaults to an empty dictionary  
- `fun`: Function type, used to process requests and responses, accept two inputs `req` and `dict` and return two dictionary type variables `msg` and `dict`  
- `dict`: Dictionary type, used to store information required by programs and frameworks. Can be updated via `fun` as needed, such as adding shared data for multiple connections. If no updates, `fun` should return the same dictionary as the input. In the following example, all uppercase keys are internal parameters of the framework and should not be modified, and lowercase keys are parameters required by the program.  
    ```python
    {
        'SVRIP': 'localhost',
        'SVRPORT': 1080,
        'WS': {},
        ... ...
        'param1': 1,
        'param2': 2,
    }
    ```
    
- `req`: Dictionary type, containing request information, the content varies by protocol, see following example  
    ```python
    {
        'version': ,
    }
    ```
- `msg`: Dictionary type, containing the information that needs to be sent, see following example
    ```python
    {
        'version': ,
    }
    ```
## HTTP
### Requset
```python
{
    'addr': ('127.0.0.1', 33342),
    'method': 'GET',
    'target': '/',
    'version': 'HTTP/1.1',
    'Host': 'localhost:1080',
    'Connection': 'keep-alive',
    'Content-Length': 0,
    'Accept': 'image/avif,image/webp',
    'body': '',
}
```
### Response
## WebSocket
### Receive
```python
{
    'FIN': 1
    'RSV': 0
    'opcode': 1
    'MASK': 1
    'length': 0
    'KEY': b'\xce\xc5\xc2\x86'
    'body': ''
}
```
### Send
### Push
## Example
