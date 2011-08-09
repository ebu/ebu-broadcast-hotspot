from xml.etree import ElementTree as ET

VERSION = "0.1"

def capabilities(servicelist):
    root = ET.Element("xml")
    root.attrib['encoding'] = 'utf-8'
    
    version = ET.SubElement(root, "version")
    version.text = VERSION

    services = ET.SubElement(root, "services")
    for serv in servicelist:
        serv_el = ET.SubElement(services, "service")
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
