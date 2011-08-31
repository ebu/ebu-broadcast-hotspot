/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.radiodns;

/**
 * Declares the callback functions which are called by the RadioVIS receiver
 * @author mpb
 *
 */
public interface RadioVisCallbacks {
	/**
	 * A new SHOW has been received, and its URL points to a picture the receiver has to show.
	 * @param Url
	 */
	public void newSHOW(String imageUrl, String linkUrl);
	
	/**
	 * A new TEXT has been received, and should be printed on the screen.
	 * @param Text
	 */
	public void newTEXT(String text);
}
