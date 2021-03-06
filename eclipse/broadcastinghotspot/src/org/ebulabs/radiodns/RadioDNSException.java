/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.radiodns;

public class RadioDNSException extends Exception {
	private static final long serialVersionUID = -1427377500294846598L;
	
	private Exception inner;

	public RadioDNSException() {
		super();	
	}
	
	public RadioDNSException(String detailMessage) {
		super(detailMessage);	
	}

	public RadioDNSException(Exception inner) {
		super();
		this.inner = inner;
	}

	public Exception getInnerException() {
		return this.inner;
	}
}