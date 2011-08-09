# This file contains all code needed to talk
# to the receiving devices.
#
# What is required:
# - get/set the frequency
# - define which programme to receive
# - get additional programme info (EPG, PI for FM, ...)
# - enable/disable streaming, and get corresponding url
# - (and therefore, control the the streaming program)

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

    def get_frequency_list(self):
        return [0]

    def get_frequency(self):
        return 0

    def set_frequency(self, frequency):
        pass

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
    def get_frequency_list(self):
        return [223936000]

class DVBController(DeviceController):
    def __init__(self):
        self.dev_id = "/dev/dvb/adapter0/"
    def get_frequency_list(self):
        return [578000000]
