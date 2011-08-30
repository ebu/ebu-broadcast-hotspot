/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.util.ArrayList;

public class Device {
	public String id;
	public ArrayList<Long> frequencies;
	
	public Device (String id) {
		this.id = id;
		this.frequencies = new ArrayList<Long>();
	}
	
	public void addFrequency(long freq) {
		this.frequencies.add(freq);
	}
}
