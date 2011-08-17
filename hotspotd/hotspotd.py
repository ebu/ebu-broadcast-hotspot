#!/usr/bin/env python

"""EBU Hotspot Daemon

Communicates with user device"""

from xml.etree import ElementTree as ET
from tech import *

from misc import capabilities

import BaseHTTPServer
import urlparse

# The urls must be http://host/hotspot/<something>
base_url = "hotspot"

class HotspotHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_post_and_get('GET')
        
    def do_POST(self):
        return self.do_post_and_get('POST')

    def do_post_and_get(self, method):
        # convenience
        get = (method == 'GET')
        post = (method == 'POST')

        parsed_url = urlparse.urlparse(self.path)

        p = parsed_url.path.split('/')

        if p[1] != base_url:
            print(p)
            self.send_error(404)
            return

        if p[2] == "capabilities":
            if get:
                message = capabilities(techlist)
                self.send_response(200)
                self.send_header("Content-Type", "text/xml")
            if post:
                self.send_error(405) # method not allowed
                return

        elif p[2] in [str(i) for i in techlist]:
            if len(p) < 4:
                self.send_response(400) # Bad Request
                message = ""
            else:
                cmd = p[3]
                s = name_to_tech(p[2])

                if cmd == "frequency":
                    if get:
                        freq = s.devices[0].get_frequency()
                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain")

                        message = str(freq)

                    if post:
                        content_length = int(self.headers.getheader('Content-Length'))
                        if content_length == 0:
                            print("Content length is zero !")

                        freq = self.rfile.read(content_length)
                        print("new frequency {0}".format(freq))

                        try:
                            s.devices[0].set_frequency(int(freq))
                        except ValueError:
                            self.send_error(400)
                            return
                        message = ""

                elif cmd == "programmes": # list of programmes
                    if get:
                        programmes = s.devices[0].get_programme_list()
                        root = ET.Element("xml")
                        root.attrib['encoding'] = 'utf-8'
                        
                        for p in programmes:
                            p_el = ET.SubElement(root, "programme")
                            p_el.text = p
                        message = ET.tostring(root, encoding="utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "text/xml")
                    if post:
                        self.send_error(405) # method not allowed
                        return

                elif cmd == "programme": # current programme
                    if get:
                        programme = s.devices[0].get_programme()
                        root = ET.Element("xml")
                        root.attrib['encoding'] = 'utf-8'
                        
                        p_el = ET.SubElement(root, "programme")
                        p_el.attrib['name'] = programme

                        url_el = ET.SubElement(p_el, "url")
                        url_el.text = s.devices[0].get_stream_url()

                        info_el = ET.SubElement(p_el, "info")
                        s.devices[0].fill_additional_info(info_el)

                        message = ET.tostring(root, encoding="utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "text/xml")
                    if post:
                        content_length = int(self.headers.getheader('Content-Length'))
                        if content_length == 0:
                            print("programme: Content length is zero !")

                        programme = self.rfile.read(content_length)
                        print("new programme {0}".format(programme))

                        if not s.devices[0].set_programme(programme):
                            self.send_error(400)
                            return

                        message = str(s.devices[0].start_stream())
                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain")

                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/plain")
                    message = ""




        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            message = '\n'.join([
                '<html><head><title>Hotspot</title></head>',
                '<body>',
                '<h1>EBU Hotspot</h1>',
                '<a href="/hotspot/capabilities">capabilities</a><br />',
                '<a href="/hotspot/DAB/programmes">DAB programme list</a><br />',
                '<a href="/hotspot/DAB/programme">DAB programme info</a><br />',
                '<a href="/hotspot/DAB/frequency">DAB frequency info</a><br />',
                '<p>',
                'cmd {0},',
                'path {1},',
                'query {2},',
                'raw path {3},',
                "</p>"]).format(self.command, parsed_url.path, parsed_url.query, self.path)

        self.end_headers()
        self.wfile.write(message)
        

if __name__ == "__main__":
    s = BaseHTTPServer.HTTPServer(('0.0.0.0', 8080), HotspotHandler)
    print("Starting Hotspotd HTTP server")
    s.serve_forever()
        
