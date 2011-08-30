package org.ebulabs.hotspot;

import java.util.Map;

import android.util.Log;

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

	/** XML-encoded additional data */
	private Map<String, String> info;

	public Map<String, String> getInfo() {
		return info;
	}

	public void setInfo(Map<String, String> info) {
		this.info = info;
	}
}
