#!/usr/bin/python3

# Implements a simple XMLRPC server for test purposes
# 26.03.2010 Bram

from xmlrpc.server import DocXMLRPCServer
from xmlrpc.server import DocXMLRPCRequestHandler

class RequestHandler(DocXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = DocXMLRPCServer(("0.0.0.0", 2720), requestHandler=RequestHandler)

# gives access to system.listMethods, system.methodHelp and system.methodSignature
server.register_introspection_functions()

def reverse(x):
    return "".join(list(reversed(x)))

def get():
    return ["Power", "Energy", "Force", "Distance", "Current", "Apple pies"]

print("Registering functions")
server.register_function(reverse, 'reverse')
server.register_function(get, 'get')

print("Ready")
server.serve_forever()
