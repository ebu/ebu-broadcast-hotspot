#!/usr/bin/env python

"""EBU Hotspot Daemon

Communicates with user device"""

from xml.etree import ElementTree as ET
from tech import *
from misc import *
import cgi

import BaseHTTPServer
import urlparse

# The urls must be http://host/hotspot/<something>
base_url = "hotspot"
help_message = '\n'.join([
        '<html><head><title>Hotspot</title></head>',
        '<body>',
        '<h1>EBU Hotspot</h1>',
        '<a href="/hotspot/capabilities">capabilities</a><br />',
        '<a href="/hotspot/DAB/programmes">DAB programme list</a><br />',
        '<a href="/hotspot/DAB/programme">DAB programme info</a><br />',
        '<a href="/hotspot/DAB/frequency">DAB frequency info</a><br />',
        '<a href="/hotspot/DAB/reload">DAB Reload</a><br />',
        '<form method="post" action="/hotspot/DAB/frequency"><p>',
        'Frequency : <input type="text" name="value" value="223936000" />',
        '<input type="submit" value="Set DAB Frequency" />',
        '</p></form>',
        '<form method="post" action="/hotspot/DAB/programme"><p>',
        'Frequency : <input type="text" name="value" value="ESPACE 2" />',
        '<input type="submit" value="Set DAB Programme" />',
        '</p></form>'
        
        ])

class HotspotState:
    programme = None

class HotspotHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """This class handles HTTP requests to control the hotspot.

    For now, it is stateful, and remembers what programme the user has chosen.
    In a multi-user system, this would have to be changed."""

    def do_GET(self):
        return self.do_post_and_get('GET')
        
    def do_POST(self):
        post_content_type = self.headers.getheader('Content-Type')

        content_length = int(self.headers.getheader('Content-Length'))
        if content_length == 0:
            print("Content length is zero !")

        if post_content_type == "application/x-www-form-urlencoded":
            form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

            post_data = form['value'].value
        else:
            post_data = self.rfile.read(content_length)

        return self.do_post_and_get('POST', post_data)

    def do_post_and_get(self, method, post_data=""):
        # convenience
        get = (method == 'GET')
        post = (method == 'POST')

        parsed_url = urlparse.urlparse(self.path)

        p = parsed_url.path.split('/')

        if p[1] != base_url:
            print(p)
            self.send_error(404)
            return

        if len(p) == 2:
            message = help_message
            self.send_response(200)
            self.send_header("Content-Type", "text/html")

        elif p[2] == "capabilities":
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
                        freq = post_data
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
                        root = ET.Element("xml")
                        root.attrib['encoding'] = 'utf-8'
                        
                        p_el = ET.SubElement(root, "programme")
                        url_el = ET.SubElement(p_el, "url")
                        info_el = ET.SubElement(p_el, "info")

                        if HotspotState.programme is not None:
                            p_el.attrib['name'] = HotspotState.programme
                            url_el.text = s.devices[0].get_stream_url(HotspotState.programme)
                            s.devices[0].fill_additional_info(HotspotState.programme, info_el)
                        else:
                            p_el.attrib['name'] = ""

                        message = ET.tostring(root, encoding="utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "text/xml")
                    if post:
                        HotspotState.programme = post_data
                        print("new programme {0}".format(HotspotState.programme))

                        if not s.devices[0].start_stream(HotspotState.programme):
                            self.send_error(400)
                            return

                        message = s.devices[0].get_stream_url(HotspotState.programme)

                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain")

                elif cmd == "reload": # reload the tech
                    if get: # TODO, should be POST
                        message = s.reload()
                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain")

                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/plain")
                    message = ""




        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            message = help_message

        self.end_headers()
        self.wfile.write(message)
        

if __name__ == "__main__":
    s = BaseHTTPServer.HTTPServer(('0.0.0.0', 8080), HotspotHandler)
    print("Starting Hotspotd HTTP server")
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("Leaving")
        print("")
        [t.shutdown() for t in techlist]
        
