#!/usr/bin/env python

"""EBU Hotspot Daemon

Communicates with user device"""

from xml.etree import ElementTree as ET
from tech import *
from misc import *
from avahi_publish import AvahiPublisherThread
import cgi

import BaseHTTPServer
import urlparse

tech_links = '\n'.join([
        '<h2>Technology: {tech}</h2>',
        '<p>',
        '<a href="/{tech}/programmes">{tech} programme list</a><br />',
        '<a href="/{tech}/programme">{tech} programme info</a><br />',
        '<a href="/{tech}/frequency">{tech} frequency info</a><br />',
        '<a href="/{tech}/reload">Reload/Restart {tech}</a><br />',
        '<form method="post" action="/{tech}/frequency"><p>',
        'Frequency : <input type="text" name="value" value="223936000" />',
        '<input type="submit" value="Set {tech} Frequency" />',
        '</p></form>',
        '<form method="post" action="/{tech}/programme"><p>',
        'Programme : <input type="text" name="value" value="" />',
        '<input type="submit" value="Set {tech} Programme" />',
        '</p></form>'
        '</p>'])
        
help_message_header = '\n'.join([
        '<html><head><title>Hotspot</title></head>',
        '<body style="font-family:verdana; color:#555">',
        '<a href="http://tech.ebu.ch">',
        '<img src="http://www.ebulabs.org/radiovismanager/img/ebulogo.png" border=0 style="float:left; padding-right:30px;">',
        '</a>',
        '<h1>EBU Broadcast Hotspot</h1>',
        '<p><b>Debugging access through browser</b></p>',
        '<p>This hotspot can be controlled with the <i>EBU BC Hotspot</i> android application.</p>',
        '<p>Please refer to <a href="http://www.ebulabs.org">ebulabs.org</a> for more details.</p>',
        '<h2>Technology independant</h2>',
        '<a href="/capabilities">capabilities</a><br />',
        ])

help_message = help_message_header + "\n".join([tech_links.format(tech=t) for t in sorted(techlist)])

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
            self.send_error(400)
            return

        return self.do_post_and_get('POST', post_data)

    def do_post_and_get(self, method, post_data=""):
        # convenience
        get = (method == 'GET')
        post = (method == 'POST')

        parsed_url = urlparse.urlparse(self.path)

        p = parsed_url.path.split('/')

        if len(p) == 1:
            message = help_message
            self.send_response(200)
            self.send_header("Content-Type", "text/html")

        elif p[1] == "capabilities":
            if get:
                message = capabilities(techlist)
                self.send_response(200)
                self.send_header("Content-Type", "text/xml")
            if post:
                self.send_error(405) # method not allowed
                return

        elif p[1] in [str(i) for i in techlist]:
            if len(p) < 3:
                self.send_response(400) # Bad Request
                message = ""
            else:
                cmd = p[2]
                s = name_to_tech(p[1])
                try:
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
                            root = ET.Element("programmes")
                            
                            for pr in programmes:
                                p_el = ET.SubElement(root, "programme")
                                p_el.text = pr
                            message = xml_prolog + ET.tostring(root, encoding="utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "text/xml")
                        if post:
                            self.send_error(405) # method not allowed
                            return

                    elif cmd == "programme": # current programme
                        if get:
                            root = ET.Element("programme")
                            
                            name_el = ET.SubElement(root, "name")
                            url_el = ET.SubElement(root, "url")
                            info_el = ET.SubElement(root, "info")

                            if HotspotState.programme is not None:
                                name_el.text = HotspotState.programme
                                url_el.text = s.devices[0].get_stream_url(HotspotState.programme)
                                s.devices[0].fill_additional_info(HotspotState.programme, info_el)

                            message = xml_prolog + ET.tostring(root, encoding="utf-8")
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
                except NotImplementedError as e:
                        self.send_response(400)
                        self.send_header("Content-Type", "text/plain")
                        message = "Functionality not implemented!"





        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            message = help_message

        self.end_headers()
        self.wfile.write(message)
        

if __name__ == "__main__":
    s = BaseHTTPServer.HTTPServer(('0.0.0.0', HOTSPOT_PORT), HotspotHandler)
    print("Starting Hotspotd")
    # Publish the hotspot over Zeroconf
    pub = AvahiPublisherThread()
    pub.start()
    print("Starting HTTP server")
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print("Leaving")
        print("")
        [t.shutdown() for t in techlist]
    finally:
        pub.stop()
        
