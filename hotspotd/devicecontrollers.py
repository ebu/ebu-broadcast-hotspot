# This file is part of the EBU Broadcast Hotspot
# Copyright (c) 2011 European Broadcasting Union
# http://www.ebulabs.org
#
# LICENSE: see LICENSE

# This file contains all code needed to talk
# to the receiving devices.
#
# What is required:
# - get/set the frequency
# - define which programme to receive
# - get additional programme info (EPG, PI for FM, ...)
# - enable/disable streaming, and get corresponding url
# - (and therefore, control the the streaming program)

from openmokast_dbus_remote import *
from openmokast_to_icecast import OpenMokastIceCastAdapter
from openmokast_to_vlc import OpenMokastVLCAdapter
from xml.etree import ElementTree as ET
from urlparse import urlparse
import time
from misc import *
from dabfreq import dab_channels

localhost = "127.0.0.1"

class DeviceController(object):
    """Abstract class defining what functions a device controller has to implement.
    
    Each device might receive several programme at once on one frequency."""

    def __init__(self):
        self.dev_id = None

    def reload(self):
        raise NotImplementedError()

    # return the dictionary of channels: frequency
    def get_frequency_list(self):
        raise NotImplementedError()

    def get_frequency(self):
        raise NotImplementedError()

    def set_frequency(self, frequency):
        raise NotImplementedError()

    def get_programme_list(self):
        raise NotImplementedError()

    def fill_additional_info(self, programme, info_element):
        raise NotImplementedError()

    def get_stream_url(self, programme):
        raise NotImplementedError()

    def start_stream(self, programme):
        raise NotImplementedError()

    def stop_stream(self, programme):
        raise NotImplementedError()

    def shutdown(self):
        raise NotImplementedError()

class DummyController(DeviceController):
    """Does nothing. But does not crash either"""
   
    def __init__(self):
        self.dev_id = "dummy0"
        self._freq = 0
        self._programme = "foo"

    def reload(self):
        return "Nothing to do"

    def get_frequency_list(self):
        return {'0': 0}

    def get_frequency(self):
        return self._freq

    def set_frequency(self, frequency):
        self._freq = frequency

    def get_programme_list(self):
        return ["foo", "bar"]

    def fill_additional_info(self, programme, info_element):
        eid_el = ET.SubElement(info_element, "comment")
        eid_el.text = "No additional info available for dummy device"

    def get_stream_url(self, programme):
        return ""

    def start_stream(self, programme):
        return True

    def stop_stream(self, programme):
        return True

    def shutdown(self):
        return True
    

class DABController(DeviceController):
    def __init__(self):
        self.dev_id = "dab0"

        self.rc = OpenmokastReceiverRemote()
        
        # keys: programmes
        self._adapters = {} 

        #self.set_frequency(self.get_frequency_list()[0]) # tune to first available freq
        #try:
        #    print(self.rc.start_decoding_programme("COULEUR 3"))
        #except ProgrammeNotInEnsembleError:
        #    print("COULEUR 3 not found")

    def get_frequency_list(self):
        return dab_channels

    def reload(self):
        self.rc = OpenmokastReceiverRemote()

        for a in self._adapters.values():
            a.stop()

        self._adapters = {}

        return "Reloaded"

    def set_frequency(self, frequency):
        Log.i("devctrl", "Tuning openmokast to {0} Hz".format(frequency))
        self.rc.tune(frequency)

    def get_frequency(self):
        return self.rc.get_frequency()

    def get_programme_list(self):
        ens = self.rc.get_ensemble()
        #print("Ensemble: {0}".format(ens))
        return ens

    def fill_additional_info(self, programme, info_element):
        try:
            sid, subchid = self.rc.get_programme_data(programme)
        except ProgrammeNotInEnsembleError:
            return False

        eid = self.rc.get_ensemble_id()

        eid_el = ET.SubElement(info_element, "eid")
        eid_el.text = str(int(eid))

        sid_el = ET.SubElement(info_element, "sid")
        sid_el.text = str(int(sid))

        subch_el = ET.SubElement(info_element, "subchid")
        subch_el.text = str(int(subchid))
        return True
        

    def get_stream_url(self, programme):
        Log.d("devctrl", "DAB get stream URL")
        if programme is None:
            return None

        if programme in self._adapters:
            Log.d("devctrl", "DAB stream URL is {0}".format(self._adapters[programme].get_url()))
            return self._adapters[programme].get_url()
        else:
            return ""

    def start_stream(self, programme):
        Log.d("devctrl", "DAB start stream (stop_decoding_programme, set_destination, start_decoding_programme)")
        if programme is None:
            return False
        else:
            eid, subch = self.rc.get_programme_data(programme)
            self.stop_stream(programme)
            time.sleep(1)

            if OPENMOKAST_UDP:
                proto = "udp"
            elif OPENMOKAST_TCP:
                proto = "tcp"
            elif OPENMOKAST_HTTP:
                proto = "http"
            else:
                raise Exception("Openmoko protocol not defined!")

            om_port = 40000 + subch

            self.rc.set_destination(programme, localhost, om_port, proto)
            openmokast_destination = self.rc.start_decoding_programme(programme)
            Log.d("devctrl", "OM streams to {0}".format(openmokast_destination))

            if ADAPTER_ICECAST:
                mountpoint = programme.replace(" ", "_")
                om_port = urlparse(openmokast_destination).port

                Log.d("devctrl", "Mountpoint {0}, om_port {1}".format(mountpoint, om_port))

                a = OpenMokastIceCastAdapter(om_port, mountpoint)

            elif ADAPTER_VLC:
                vlc_port = om_port + 10000
                access = "0.0.0.0"

                # takes care of protocol details etc...
                a = OpenMokastVLCAdapter(openmokast_destination, VLC_PROTOCOL, access, vlc_port, "audio", codec=VLC_CODEC)

            self._adapters[programme] = a

            Log.d("devctrl", "URL: {0}".format(a.get_url()))

            a.start()

            return a.get_url()

    def stop_stream(self, programme):
        if programme in self._adapters:
            self._adapters[programme].stop()

        self.rc.stop_decoding_programme(programme)


    def shutdown(self):
        for a in self._adapters.values():
            a.stop()


class DVBController(DeviceController):
    def __init__(self):
        self.dev_id = "/dev/dvb/adapter0/"
    def get_frequency_list(self):
        return {'34': 578000000}
    def shutdown(self):
        pass
