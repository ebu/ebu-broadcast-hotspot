/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

public class HotspotException extends Exception {

	private static final long serialVersionUID = 3419216738510591787L;
	
	private Exception inner;
	
	public HotspotException() {
		super();
	}
	
	public HotspotException(String detailMessage) {
		super(detailMessage);
	}
	
	public HotspotException(Exception inner) {
		super();
		this.inner = inner;
	}

	public Exception getInnerException() {
		return this.inner;
	}

}
