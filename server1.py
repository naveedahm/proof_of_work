from jsonrpctcp.server import Server
from jsonrpctcp import config

config.verbose = True

def add(x, y):
    return x+y
    
def echo(message):
    return message
    
server = Server(('localhost', 8001))
server.add_handler(add)
server.add_handler(echo, 'namespace.echo')
server.serve() # blocks

