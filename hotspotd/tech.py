# Definition of the different techs

import devicecontrollers as dc
############################### {{{
# tech capabilities constants

CAP_VIDEO = "video"
CAP_AUDIO = "audio"
CAP_SLIDESHOW = "slideshow"

############################### }}}

# Techs:
class Tech(object):
    """Represents a tech. Each tech can have several devices."""
    def __init__(self, name, devices, capabilities):
        self.name = name
        self.devices = devices
        self.capabilities = capabilities

    # Be careful to have unique names !
    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

# some example techs, can be considered as singletons
DVB = Tech('DVB', [dc.DVBController()], [CAP_VIDEO, CAP_AUDIO])
DAB = Tech('DAB', [dc.DABController()], [CAP_AUDIO, CAP_SLIDESHOW])
Dummy = Tech('Dummy', [dc.DummyController()], [CAP_AUDIO])

techlist = [DVB, DAB, Dummy]

def name_to_tech(servname):
    servs = filter(lambda x: x.name == servname, techlist)
    if len(servs) == 1:
        return servs[0]
    else:
        raise IndexError("Tech '{0}' not in list".format(servname))

############################### }}}

