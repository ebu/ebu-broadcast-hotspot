/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

import android.util.Log;


class ProgrammeInfoHandler extends DefaultHandler {

	StringBuilder currentCharacter;
	
	Map<String,String> infoFields;
	String url;
	String name;
	boolean enableInfo;

	public ProgrammeInfoHandler() {
		super();
		this.infoFields = new HashMap<String, String>();
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
		if (localName == "url") {
			this.url = currentCharacter.toString();
		}
		else if (localName == "info") {
			this.enableInfo = false;
			currentCharacter = new StringBuilder();
		}
		else if (localName == "name") {
			this.name = currentCharacter.toString();
			currentCharacter = new StringBuilder();
		}
		else if (this.enableInfo) {
			infoFields.put(localName, currentCharacter.toString());
			currentCharacter = new StringBuilder();
		}
	}
	
	@Override
	public void startElement(String namespaceURI, String localName, String qName, 
		    Attributes atts) throws SAXException {
		Log.d(Utils.LOGTAG + "startElement", localName);
		
		if (localName == "name") {
			currentCharacter = new StringBuilder();
		}
		
		if (localName == "info") {
			this.enableInfo = true;
			currentCharacter = new StringBuilder();
		}

	}
	
	@Override
	public void characters(char ch[], int start, int length) {
		currentCharacter.append(ch, start, length);
	}
}

public class XMLProgrammeInfoParser {

	public ProgrammeInfo pi;
	
	public XMLProgrammeInfoParser(InputStream s) throws HotspotException {
		SAXParserFactory spf = SAXParserFactory.newInstance();
		SAXParser sp;
		
		try {
			sp = spf.newSAXParser();
		
			XMLReader xr  = sp.getXMLReader();
			
			ProgrammeInfoHandler h = new ProgrammeInfoHandler();
			xr.setContentHandler(h);
			
			xr.parse(new InputSource(s));
			
			pi = new ProgrammeInfo(h.name, h.url);
			pi.setInfo(h.infoFields);
		}
		catch (Exception e) {
			e.printStackTrace();
			throw new HotspotException(e);
		}
		
	}
}
