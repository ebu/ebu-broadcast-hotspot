/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.io.InputStream;
import java.util.ArrayList;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;
import android.util.Log;

/**
 * Parser for the capabilities XML
 * @author mpb
 *
 */
class CapabilitiesHandler extends DefaultHandler {
	
	ArrayList<Tech> techs;
	
	Tech currentTech;
	Device currentDev;
	StringBuilder currentCharacter;
	
	public CapabilitiesHandler() {
		super();
		techs = new ArrayList<Tech>();
	}
	
	@Override
	public void startDocument() throws SAXException {
		currentCharacter = new StringBuilder();
	}
	@Override
	public void endDocument() throws SAXException { }
	
	@Override
	public void endElement(String namespaceURI, String localName, String qName) 
    throws SAXException {
		if (localName == "tech") {
			techs.add(currentTech);
		}
		else if (localName == "device") {
			currentTech.addDevice(currentDev);
		}
		else if (localName == "capability") {
			currentTech.addCapability(currentCharacter.toString());
		}
		else if (localName == "frequency") {
			currentDev.addFrequency(Long.parseLong(currentCharacter.toString()));
		}
	}
	
	@Override
	public void startElement(String namespaceURI, String localName, String qName, 
		    Attributes atts) throws SAXException {
		if (localName == "tech") {
			String techname = atts.getValue("", "name");
			if (techname == null) {
				Log.e(Utils.LOGTAG + "startElement", "tech name is null");
				throw new SAXException("Tech has no name");
			}
			
			currentTech = new Tech(techname);
			
		}
		else if (localName == "device") {
			String devid = atts.getValue("", "id");
			if (devid == null) {
				Log.e(Utils.LOGTAG + "startElement", "device name is null");
				throw new SAXException("Device has no name");
			}
			
			currentDev = new Device(devid);
			currentCharacter = new StringBuilder();
		}
		else if (localName == "capability") {
			currentCharacter = new StringBuilder();
		}
		else if (localName == "frequency") {
			currentCharacter = new StringBuilder();
		}
	}
	
	@Override
	public void characters(char ch[], int start, int length) {
		currentCharacter.append(ch, start, length);
	}
}

public class XMLCapabilitiesParser {
	
	public ArrayList<Tech> techs;
	
	public XMLCapabilitiesParser(InputStream s) throws HotspotException {
		SAXParserFactory spf = SAXParserFactory.newInstance();
		SAXParser sp;
		try {
			sp = spf.newSAXParser();
		
			XMLReader xr  = sp.getXMLReader();
			
			CapabilitiesHandler h = new CapabilitiesHandler();
			xr.setContentHandler(h);
			
			xr.parse(new InputSource(s));
			
			techs = h.techs;
			
		} catch (Exception e) {
			
			e.printStackTrace();
			throw new HotspotException(e);
		}
		
		
	}
}
