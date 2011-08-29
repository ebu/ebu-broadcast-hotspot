package org.ebulabs.hotspot;

public class HotspotException extends Exception {

	private static final long serialVersionUID = 3419216738510591787L;
	
	private Exception inner;
	
	public HotspotException() {}
	
	public HotspotException(Exception inner) {
		this.inner = inner;
	}

	public Exception getInnerException() {
		return this.inner;
	}

}