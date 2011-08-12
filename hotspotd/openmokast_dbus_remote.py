#!/usr/bin/env python
from time import sleep
import dbus

rx_name = "org.openmokast.Receiver"
rx_object_path = "/org/openmokast/Receiver"
srg_ensemble_freq = 223936000

udp_dest = "239.10.10.1"

class ProgrammeNotInEnsembleError(Exception):
    pass

class OpenmokastReceiverRemote(object):

    def __init__(self):
        self.o = self._getControlObject()

    def _getControlObject(self):
        """Connect to dbus and initialise object to talk with
        openmokast"""
        bus = dbus.SessionBus()
        obj = bus.get_object(rx_name, rx_object_path)

        return obj

    def tune(self, frequency):
        """Tune to the specified frequency given in Hz"""
        mode = 1
        self.o.Tune(dbus.UInt32(frequency / 1000), dbus.UInt32(mode))

    def get_frequency(self):
        f = self.o.GetFrequency()
        return 1000 * int(f[0])

    def getstatus(self):
        print(str(self.o.GetStatus()))

    def get_ensemble(self):
        services = self.o.GetServiceArray()
        return [str(j).strip() for j in services[1]]


    def get_programme_data(self, programme):
        """Get the service id, the component id for the specified programme"""
        services = self.o.GetServiceArray()
        servicenames = [s.strip() for s in services[1]]
        #print("check if {0} in {1}".format(programme, servicenames))
        if programme not in servicenames:
            raise ProgrammeNotInEnsembleError("Programme '{0}' not found in ensemble '{1}'".format(
                programme, servicenames))

        serviceid = services[0][servicenames.index(programme)]

        components = self.o.GetComponentArray(serviceid)

        return serviceid, components[0][0] #default channel

    def print_programme_transport_mode(self, programme):
        sid, compid = self.get_programme_data(programme)

        tm, _ = self.o.GetTransportMode(sid, compid)

        tmodes = {0: "AUDIO STREAM",
                1: "DATA STREAM",
                2: "FIDC SERVICE",
                3: "DATA PACKET SERVICE"}

        if tm in tmodes:
            print(tmodes[tm])
        else:
            print("Unknown transport mode " + str(tm))

    def set_destination(self, programme, destination_ip, destination_port, proto):
        #setdestination 16449 17313 10    239.10.10.1 2720 udp
        #               EId   SId   subch
        eid = self.o.GetEnsemble()[0]
        sid, subch = self.get_programme_data(programme)

        self.o.SetDestination(eid, sid, subch, destination_ip, dbus.UInt32(destination_port), proto)



    def start_decoding_programme(self, programme):
        destination = self.o.StartDecoding(*self.get_programme_data(programme))[0]

        return str(destination)

    def stop_decoding_programme(self, programme):
        success = self.o.StopDecoding(*self.get_programme_data(programme))

        return success

