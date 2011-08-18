from xml.etree import ElementTree as ET

VERSION = "0.1"

myip = "192.168.1.114"

def capabilities(techlist):
    root = ET.Element("xml")
    root.attrib['encoding'] = 'utf-8'
    
    version = ET.SubElement(root, "version")
    version.text = VERSION

    techs = ET.SubElement(root, "techs")
    for serv in techlist:
        serv_el = ET.SubElement(techs, "tech")
        serv_el.attrib["name"] = serv.name

        for cap in serv.capabilities:
            cap_el = ET.SubElement(serv_el, "capability")
            cap_el.text = cap

        for d in serv.devices:
            serv_devs = ET.SubElement(serv_el, "device")
            serv_devs.attrib["id"] = d.dev_id
            for f in d.get_frequency_list():
                freq_el = ET.SubElement(serv_devs, "frequency")
                freq_el.text = str(f)
    
    return ET.tostring(root, encoding="utf-8")

class Colour:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class Log(object):
    LEVEL = 4

    DEBUG = 4
    INFO = 3
    WARN = 2
    ERR = 1

    @staticmethod
    def d(src, message):
        if Log.LEVEL >= Log.DEBUG:
            print(Colour.PURPLE + "DEBUG: {0}: {1}".format(src, message) + Colour.ENDC)

    @staticmethod
    def p(src, message):
        """Use this as print function"""
        print(Colour.GREEN + "{0}: {1}".format(src, message) + Colour.ENDC)

    @staticmethod
    def i(src, message):
        if Log.LEVEL >= Log.INFO:
            print(Colour.BLUE + "INFO: {0}: {1}".format(src, message) + Colour.ENDC)

    @staticmethod
    def w(src, message):
        if Log.LEVEL >= Log.WARN:
            print(Colour.YELLOW + "WARN: {0}: {1}".format(src, message) + Colour.ENDC)

    @staticmethod
    def e(src, message):
        if Log.LEVEL >= Log.ERR:
            print(Colour.RED + "ERROR: {0}: {1}".format(src, message) + Colour.ENDC)

