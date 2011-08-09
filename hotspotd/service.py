# Definition of the different services

import devicecontrollers as dc
############################### {{{
# service capabilities constants

CAP_VIDEO = "video"
CAP_AUDIO = "audio"
CAP_SLIDESHOW = "slideshow"

############################### }}}

# Services:
class Service(object):
    """Represents a service. Each service can have several devices."""
    def __init__(self, name, devices, capabilities):
        self.name = name
        self.devices = devices
        self.capabilities = capabilities

    # Be careful to have unique names !
    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

# some example services, can be considered as singletons
DVB = Service('DVB', [dc.DVBController()], [CAP_VIDEO, CAP_AUDIO])
DAB = Service('DAB', [dc.DABController()], [CAP_AUDIO, CAP_SLIDESHOW])
Dummy = Service('Dummy', [dc.DummyController()], [CAP_AUDIO])

servicelist = [DVB, DAB, Dummy]

############################### }}}


############################### {{{
