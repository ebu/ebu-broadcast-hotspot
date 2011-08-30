/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.util.Map;

import android.util.Log;

/**
 * Contains all information for a programme.
 * @author mpb
 *
 */
public class ProgrammeInfo {
	
	public ProgrammeInfo(String name) {
		this(name, "");
	}
	
	public ProgrammeInfo(String name, String url) {
		this.name = name;
		this.url = url;
		Log.d(Utils.LOGTAG + "ProgrammeInfo", "Setting up " + name + ", " + url);
	}
	
	/** Name of the programme */
	public String name;

	/** URL where we can receive the programme */
	public String url;

	/** additional data from the XML programme info */
	private Map<String, String> info;

	public Map<String, String> getInfo() {
		return info;
	}

	public void setInfo(Map<String, String> info) {
		this.info = info;
	}
}
