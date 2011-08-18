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
from xml.etree import ElementTree as ET
from urlparse import urlparse
import time
from misc import *

localhost = "127.0.0.1"

class DeviceController(object):
    """Abstract class defining what functions a device controller has to implement"""

    def __init__(self):
        self.dev_id = None

    def reload(self):
        raise NotImplementedError()

    def get_frequency_list(self):
        raise NotImplementedError()

    def get_frequency(self):
        raise NotImplementedError()

    def set_frequency(self, frequency):
        raise NotImplementedError()

    def get_programme_list(self):
        raise NotImplementedError()

    def set_programme(self, programme):
        raise NotImplementedError()

    def fill_additional_info(self):
        raise NotImplementedError()

    def get_stream_url(self):
        raise NotImplementedError()

    def start_stream(self):
        raise NotImplementedError()

    def stop_stream(self):
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
        return [0]

    def get_frequency(self):
        return self._freq

    def set_frequency(self, frequency):
        self._freq = frequency

    def get_programme_list(self):
        return ["foo", "bar"]

    def set_programme(self, programme):
        self._programme = programme
        return True

    def fill_additional_info(self):
        return "(No additional info available for dummy device)"

    def get_stream_url(self):
        return ""

    def start_stream(self):
        return True

    def stop_stream(self):
        return True
    

class DABController(DeviceController):
    def __init__(self):
        self.dev_id = "dab0"

        self.rc = OpenmokastReceiverRemote()
        
        # programme being modified or read from now
        # This assumes only one client for that controller...
        self._programme = None

        # keys: programmes
        self._destination = {}
        self._adapters = {} 

        #self.set_frequency(self.get_frequency_list()[0]) # tune to first available freq
        #try:
        #    print(self.rc.start_decoding_programme("COULEUR 3"))
        #except ProgrammeNotInEnsembleError:
        #    print("COULEUR 3 not found")

    def get_frequency_list(self):
        return [223936000]

    def reload(self):
        # TODO should we clear _destination ?
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

    def get_programme(self):
        if self._programme is None:
            return ""
        return self._programme

    def get_programme_list(self):
        ens = self.rc.get_ensemble()
        #print("Ensemble: {0}".format(ens))
        return ens

    def set_programme(self, programme):
        #print("is {0} in {1}".format(programme, self.rc.get_ensemble()))
        Log.i("devctrl", "DAB set programme to {0}".format(programme))
        if programme in self.rc.get_ensemble():
            self._programme = programme
            return True
        else:
            return False

    def fill_additional_info(self, info_element):
        try:
            sid, subchid = self.rc.get_programme_data(self._programme)
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
        

    def get_stream_url(self):
        Log.d("devctrl", "DAB get stream URL")
        if self._programme is None:
            return None

        if self._programme in self._destination:
            Log.d("devctrl", "DAB stream URL is {0}".format(self._destination[self._programme]))
            return self._destination[self._programme]
        else:
            return ""

    def start_stream(self):
        Log.d("devctrl", "DAB start stream (stop_decoding_programme, set_destination, start_decoding_programme)")
        if self._programme is None:
            return False
        else:
            eid, subch = self.rc.get_programme_data(self._programme)
            self.rc.stop_decoding_programme(self._programme)
            time.sleep(1)
            self.rc.set_destination(self._programme, localhost, 10000 + ((subch + 30000) % 55000), "udp")
            openmokast_destination = self.rc.start_decoding_programme(self._programme)
            Log.d("devctrl", "DAB stream to {0}".format(openmokast_destination))

            mountpoint = self._programme.replace(" ", "_")
            udpport = urlparse(openmokast_destination).port

            Log.d("devctrl", "Mountpoint {0}, udpport {1}".format(mountpoint, udpport))

            a = OpenMokastIceCastAdapter(udpport, mountpoint)

            self._destination[self._programme] = OpenMokastIceCastAdapter.icecast_url_prefix + mountpoint
            self._adapters[self._programme] = a

            Log.d("devctrl", "URL: {0}".format(self._destination[self._programme]))

            a.start()

            return self._destination[self._programme]

    def stop_stream(self): # who cares ?
        return self.rc.stop_decoding_programme(self._programme)


class DVBController(DeviceController):
    def __init__(self):
        self.dev_id = "/dev/dvb/adapter0/"
    def get_frequency_list(self):
        return [578000000]
