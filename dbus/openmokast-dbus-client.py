#!/usr/bin/env python
from time import sleep
import dbus

rx_name = "org.openmokast.Receiver"
rx_object_path = "/org/openmokast/Receiver"
srg_ensemble_freq = 223936

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
        """Tune to the specified frequency given in kHz"""
        mode = 1
        self.o.Tune(dbus.UInt32(frequency), dbus.UInt32(mode))

    def getstatus(self):
        print(str(self.o.GetStatus()))

    def showensemble(self):
        services = self.o.GetServiceArray()
        print("\n".join([str(i) + " " + str(j) for i,j in zip(*services[0:2])]))

        for s, name in zip(services[0], services[1]):
            print(str(name))
            components = self.o.GetComponentArray(s)
            for chan, comp_name in zip(*components[0:2]):
                print("{0}".format(chan))
        print("")

    def get_programme_data(self, programme):
        """Get the service id, the component id for the specified programme"""
        services = self.o.GetServiceArray()
        servicenames = [s.strip() for s in services[1]]
        if programme not in servicenames:
            raise ProgrammeNotInEnsembleError("Programme '{0}' not found in ensemble '{1}'".format(
                programme, self.o.GetStatus()))

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

    def start_decoding_programme(self, programme):
        destination = self.o.StartDecoding(*self.get_programme_data(programme))[0]

        return str(destination)





rc = OpenmokastReceiverRemote()
#rc.tune(srg_ensemble_freq)
#sleep(1)
rc.showensemble()
try:
    print(rc.start_decoding_programme("COULEUR 3"))
except ProgrammeNotInEnsembleError:
    print("COULEUR 3 not found")
