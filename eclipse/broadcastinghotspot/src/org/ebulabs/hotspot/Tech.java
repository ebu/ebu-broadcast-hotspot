/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.util.ArrayList;

public class Tech {
	public String name;
	public ArrayList<String> capabilities;
	
	public ArrayList<Device> devices;
	
	public Tech(String name) {
		this.name = name;
		this.capabilities = new ArrayList<String>();
		this.devices = new ArrayList<Device>();
		
	}

	public void addCapability(String cap) {
		this.capabilities.add(cap);
	}

	public void addDevice(Device dev) {
		this.devices.add(dev);
	}
}
