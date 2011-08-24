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

Log_src = "OpenMokast->VLC"

audio_params = {
        "codec_bitrate" : 320,
        "samplerate" : 48000,
        "channels" : 2,
        "codec" : "mp3",
        "container" : "mp3"}

if VLC_PROTOCOL == "HTTP":
    vlc_url_prefix = "http://"
    def vlc_destination_cmdline(destination):
        return "http{" + "dst={0}".format(destination) + "}"

elif VLC_PROTOCOL == "RTSP":
    vlc_url_prefix = "rtsp://"
    audio_params['container'] = "sdp"
    def vlc_destination_cmdline(destination):
        return "rtp{" + "dst={multicast},port={portrange},sdp=rtsp://{dst}".format(
                multicast=multicast,
                portrange="6025-6125",
                dst=destination) + "}"
else:
    Log.e("OpenMokast_to_VLC", "ERROR! VLC_PROTOCOL {0} not supported".format(VLC_PROTOCOL))
    import sys
    sys.exit(1)

def get_vlc_args(source, destination):
    transcode = "vcodec=none,acodec={codec},ab={codec_bitrate},channels={channels},samplerate={samplerate}".format(**audio_params)
    http = "dst={0}".format(destination)
    return ["cvlc", source, "--sout", "#transcode{" + transcode + "}:http{" + http + "}"] # TODO RTSP

class OpenMokastVLCAdapter(object):
    """This class implements the following command:
    cvlc -v http://localhost:40003 \
         --sout "#transcode{vcodec=none,acodec=mp3,ab=320,channels=2,samplerate=48000}:http{dst=:8080/c3.mp3}"

    used to stream openmokast to the user device. There is one adapter for each programme.
    """

    def __init__(self, om_access, destination):
        """Create a new OpenMokastVLCAdapter reading from openmokast on the URL given by 
        om_access, and transcode to destination

        Example: om_access = "http://localhost:40003"
                 destination = ":8080/audio.mp3"
        """

        Log.d(Log_src, "init")
        self.om_access = om_access
        self.destination = destination

        self.vlc = None

        self.ready = True
        self.running = False

    def __str__(self):
        return "<OM-VLC Adapter: {0} -> {1} [{2}]>".format(self.om_access, self.destination, "ready" if self.ready else "stopped")

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
        return vlc_url_prefix + self.destination

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
        args = get_vlc_args(self.om_access, self.destination)
        Log.d(Log_src, "prepare vlc\n{0}".format(args))
        self.vlc = subprocess.Popen(args)

if __name__ == "__main__":
    def p(m):
        print(Colour.GREEN + "================" + m + Colour.ENDC)

    p("TEST")

    adapt = OpenMokastVLCAdapter("http://localhost:40003", ":8080/audio.mp3")
    
    p("START")
    adapt.start()

    try:
        p("SLEEPING 60 SECS")
        time.sleep(60)
    except KeyboardInterrupt:
        pass

    p("STOPPING")
    adapt.stop()

    p("DONE")

