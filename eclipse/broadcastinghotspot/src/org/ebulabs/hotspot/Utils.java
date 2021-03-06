/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;


import android.media.AudioManager;
import android.media.MediaPlayer;
import android.util.Log;

/**
 * Some utility functions used by all activities
 * @author mpb
 *
 */
public class Utils {

	public static final String LOGTAG = "org.ebulabs.hotspot."; 
	
	/** Does a HTTP Post request to the specified url, and posts a single field called value 
	 * @throws HotspotException */
	public static HttpResponse httpPost(String url, String value) throws HotspotException {
	    // Create a new HttpClient and Post Header
	    HttpClient httpclient = new DefaultHttpClient();
	    HttpPost httppost = new HttpPost(url);

	    try {
	        // Add your data
	        List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
	        nameValuePairs.add(new BasicNameValuePair("value", value));
	        httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

	        // Execute HTTP Post Request
	        return httpclient.execute(httppost);
	        
	    } catch (Exception e) {
	    	Log.e(LOGTAG + "Utils.httpPost", "POST failed");
	    	throw new HotspotException(e);
	    }	
	}
	
    public static void startAudioStream(MediaPlayer mediaPlayer, String url) throws HotspotException { 
    	
        mediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
    
        try {
			mediaPlayer.setDataSource(url);
	        mediaPlayer.prepare(); // might take long! (for buffering, etc)
		} catch (Exception e) {
			Log.e(LOGTAG + "Utils.startAudioStream", "Failed to setup media player");
	    	throw new HotspotException(e);
	    }	
		
        mediaPlayer.start();
    }
    
    public static void stopAudioStream(MediaPlayer mediaPlayer) {
    	mediaPlayer.stop();
    }
}
