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

class ProgrammesHandler extends DefaultHandler {
	
	ArrayList<String> programmes;
	
	
	StringBuilder currentCharacter;
	
	public ProgrammesHandler() {
		super();
		programmes = new ArrayList<String>();
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
		if (localName == "programme") {
			programmes.add(currentCharacter.toString());
		}
		
	}
	
	@Override
	public void startElement(String namespaceURI, String localName, String qName, 
		    Attributes atts) throws SAXException {
		Log.d(Utils.LOGTAG + "startElement", localName);
		
		if (localName == "programme") {
			currentCharacter = new StringBuilder();
		}
	}
	
	@Override
	public void characters(char ch[], int start, int length) {
		currentCharacter.append(ch, start, length);
	}
}

public class XMLProgrammesParser {
	
	public ArrayList<String> programmes;
	
	public XMLProgrammesParser(InputStream s) throws HotspotException {
		SAXParserFactory spf = SAXParserFactory.newInstance();
		SAXParser sp;
		try {
			sp = spf.newSAXParser();
		
		
			XMLReader xr  = sp.getXMLReader();
			
			ProgrammesHandler h = new ProgrammesHandler();
			xr.setContentHandler(h);
			
			xr.parse(new InputSource(s));
			
			programmes = h.programmes;
			
		} catch (Exception e) {
			
			e.printStackTrace();
			throw new HotspotException(e);
		}
		
		
	}
}
