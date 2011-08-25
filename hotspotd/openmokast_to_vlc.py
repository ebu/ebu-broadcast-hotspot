#!/usr/bin/env python
import shlex
import subprocess
import os, os.path
import time
import threading
from misc import *

# Goal of this module:
# Get mp2 from openmokast (HTTP), feed to vlc, which transcodes and streams
# over http or RTSP

# assumes openmokast runs on localhost:
om_host = "127.0.0.1"
multicast = "139.10.10.1"
my_ip = get_ip_address()

Log_src = "OpenMokast->VLC"

audio_params_default = {
        "codec_bitrate" : 320,
        "samplerate" : 48000,
        "channels" : 2,
        "codec" : "mp3",
        "container" : "mp3"}

class OpenMokastVLCAdapter(object):
    """This class implements the following command:
    cvlc -v http://localhost:40003 \
         --sout "#transcode{vcodec=none,acodec=mp3,ab=320,channels=2,samplerate=48000}:http{dst=:8080/c3.mp3}"

    used to stream openmokast to the user device. There is one adapter for each programme.
    """

    def __init__(self, om_access, proto, access, port, filename, codec=None, ab=None):
        """Create a new OpenMokastVLCAdapter reading from openmokast on the URL given by 
        om_access, and transcode to proto://access/filename

        Example: om_access = "http://localhost:40003"
                 proto = "RTSP"
                 access = "192.168.1.114"
                 port = 554
                 filename = "foo"
              or
                 proto = "HTTP"
                 access = "192.168.1.114"
                 port = 8080
                 filename = "foo"
        Filename does not contain the filename extension, which is chosen by proto and codec
        codec and ab (audiobitrate) are optional
        """
        Log.d(Log_src, "init")

        self.audio_params = audio_params_default

        if codec is not None:
            self.audio_params['codec'] = codec
        if ab is not None:
            self.audio_params['codec_bitrate'] = ab

        if proto == "HTTP":

            #TODO consider other codecs
            if codec == "vorb":
                self.audio_params['container'] = "ogg"
            else:
                self.audio_params['container'] = self.audio_params['codec'] # works for mp3, aac, but not OGG Vorbis

            fmt = {'access':   access,
                   'filename': filename,
                   'myip':     my_ip,
                   'port':     port,
                   'ext':      self.audio_params['container']}

            self.vlc_sout_dest = "http{" + "dst={access}:{port}/{filename}.{ext}".format(**fmt) + "}"
            self.url = "http://{myip}:{port}/{filename}.{ext}".format(**fmt)

        elif proto == "RTSP":
            self.audio_params['container'] = "sdp"

            fmt = {'multicast': multicast,
                   'portrange': "6025-6125",
                   'access':    access,
                   'filename':  filename,
                   'myip':      my_ip,
                   'port':     port,
                   'ext':       self.audio_params['container']}

            self.vlc_sout_dest = "rtp{" + "dst={multicast},port={portrange},sdp=rtsp://{access}:{port}/{filename}.{ext}".format(**fmt)
            self.url = "rtsp://{myip}:{port}/{filename}.{ext}".format(**fmt)
        else:
            Log.e("OpenMokast_to_VLC", "ERROR! VLC_PROTOCOL {0} not supported".format(VLC_PROTOCOL))
            import sys
            sys.exit(1)

        self.om_access = om_access

        self.vlc = None

        self.ready = True
        self.running = False

    def get_vlc_args(self):
        transcode = "vcodec=none,acodec={codec},ab={codec_bitrate},channels={channels},samplerate={samplerate}".format(
                **self.audio_params)
        return ["cvlc", self.om_access, "--sout", "#transcode{" + transcode + "}:" + self.vlc_sout_dest]

    def __str__(self):
        return "<OM-VLC Adapter: {0} -> {1} [{2}]>".format(self.om_access, self.url, "ready" if self.ready else "stopped")

    def _destroy(self):
        Log.d(Log_src, "destroying {0}".format(self))

        self.running = False
        self.ready = False

        p = self.vlc
        # kill subprocess
        if p is not None:
            try:
                Log.d(Log_src, "terminating vlc")
                p.terminate()
            except:
                Log.e(Log_src, "Failed to term subprocess")

            time.sleep(0.5)

            try:
                rval = p.poll()
                if rval is None: # process has not terminated
                    Log.d(Log_src, "killing vlc")
                    p.kill()
            except:
                Log.e(Log_src, "Failed to kill subprocess")

        Log.i(Log_src, "{0} destroy complete".format(self))

    def stop(self):
        Log.i(Log_src, "Stopping {0}".format(self))
        self._destroy()

    def get_url(self):
        return self.url

    def start(self):
        """Start VLC.
        
        This can only be called once per instance"""

        if not self.ready:
            Log.e(Log_src, "Adapter not ready!")
            return

        # this adapter has only been tested with OM http access

        if not OPENMOKAST_HTTP:
            raise NotImplementedError("VLC adapter requires Openmokast HTTP access")

        try:
            self.prepare_vlc()
        except Exception as e:
            Log.e(Log_src, "preparation failed")
            import traceback, sys
            print(Colour.RED)
            traceback.print_exc(file=sys.stdout)
            print(Colour.ENDC)
            self._destroy()
            return

        self.running = True

    def prepare_vlc(self):
        args = self.get_vlc_args()
        Log.d(Log_src, "prepare vlc\n{0}".format(args))
        self.vlc = subprocess.Popen(args)

if __name__ == "__main__":
    def p(m):
        print(Colour.GREEN + "================" + m + Colour.ENDC)

    p("http")
    adapt_http = OpenMokastVLCAdapter("http://localhost:40003", "HTTP", "0.0.0.0:8080", "audio")

    print(adapt_http)
    print(" ".join(adapt_http.get_vlc_args()))

    p("http w/ aac")
    adapt_http = OpenMokastVLCAdapter("http://localhost:40003", "HTTP", "0.0.0.0:8080", "audio", codec="aac", ab=128)

    print(adapt_http)
    print(" ".join(adapt_http.get_vlc_args()))
    
    p("rtsp")
    adapt_rtsp = OpenMokastVLCAdapter("http://localhost:40003", "RTSP", "0.0.0.0:554", "audio")

    print(adapt_rtsp)
    print(" ".join(adapt_rtsp.get_vlc_args()))
    
    
