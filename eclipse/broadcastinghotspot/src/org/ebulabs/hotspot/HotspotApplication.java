/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.util.ArrayList;

import android.app.Application;

/**
 * The application object shared between all Activities
 * @author mpb
 *
 */
public class HotspotApplication extends Application {
	
	public String hotspotURL;
	public String ecc;
	
	public Tech activeTech;
	public ArrayList<Tech> allTechs;
	
	public ProgrammeInfo pi;
	
	public boolean enableAudio = true;

}
