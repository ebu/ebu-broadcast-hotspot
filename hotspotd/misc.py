from xml.etree import ElementTree as ET

VERSION = "0.1"

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
