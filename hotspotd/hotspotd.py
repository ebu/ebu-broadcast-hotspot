#!/usr/bin/env python

"""EBU Hotspot Daemon

Communicates with user device"""

from service import *

from misc import capabilities

import BaseHTTPServer
import urlparse
import cgi

# The urls must be http://host/hotspot/<something>
base_url = "hotspot"

class HotspotHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)

        p = parsed_url.path.split('/')

        if p[1] != base_url:
            print(p)
            self.send_error(404)
            return

        if p[2] == "capabilities":
            message = capabilities(servicelist)
            self.send_response(200)
            self.send_header("Content-Type", "text/xml")

        else:
            self.send_response(200)
            message = '\n'.join([
                'cmd {0}',
                'path {1}',
                'query {2}',
                'raw path {3}']).format(self.command, parsed_url.path, parsed_url.query, self.path)

        self.end_headers()
        self.wfile.write(message)
        

if __name__ == "__main__":
    s = BaseHTTPServer.HTTPServer(('0.0.0.0', 8080), HotspotHandler)
    print("Starting Hotspotd HTTP server")
    s.serve_forever()
        
