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

class DeviceController(object):
    """Abstract class defining what functions a device controller has to implement"""

    def __init__(self):
        self.dev_id = None

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

    def get_additional_info(self):
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

    def get_additional_info(self):
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

        self._programme = None
        self._destination = {}

        #self.set_frequency(self.get_frequency_list()[0]) # tune to first available freq
        #try:
        #    print(self.rc.start_decoding_programme("COULEUR 3"))
        #except ProgrammeNotInEnsembleError:
        #    print("COULEUR 3 not found")

    def get_frequency_list(self):
        return [223936000]

    def set_frequency(self, frequency):
        print("Tuning openmokast to {0} Hz".format(frequency))
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
        print("is {0} in {1}".format(programme, self.rc.get_ensemble()))
        if programme in self.rc.get_ensemble():
            self._programme = programme
            return True
        else:
            return False

    def get_additional_info(self):
        raise NotImplementedError()

    def get_stream_url(self):
        if self._programme is None:
            return None

        if self._programme in self._destination:
            return self._destination[self._programme]
        else:
            return ""

    def start_stream(self):
        if self._programme is None:
            return False
        else:
            self._destination[self._programme] = self.rc.start_decoding_programme(self._programme)

    def stop_stream(self): # who cares ?
        return True


class DVBController(DeviceController):
    def __init__(self):
        self.dev_id = "/dev/dvb/adapter0/"
    def get_frequency_list(self):
        return [578000000]
