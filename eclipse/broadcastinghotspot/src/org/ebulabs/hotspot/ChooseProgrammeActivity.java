package org.ebulabs.hotspot;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class ChooseProgrammeActivity extends Activity {
	
	private void toast(String t) {
		Toast.makeText(getApplicationContext(), t, Toast.LENGTH_SHORT).show();
	}
	
    /** Called when the activity is first created. */
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.programmechoice);
        
        /* Get programme list from daemon */
        
        Tech activeTech = ((HotspotApplication)getApplication()).activeTech;
        
        URL url;
        String url_sz = getString(R.string.daemon_url) + "/" + activeTech.name + "/programmes";
		try {
			url = new URL(url_sz);
		} catch (MalformedURLException e) {
			toast("Malformed URL '" + url_sz + "'");
			return;
		}
		
		Log.d("onCreate choose prog", "URL defined");
				
		ListView progList = (ListView)findViewById(R.id.programmeList);

		
        URLConnection conn;
		try {
			
			conn = url.openConnection();
			
			Log.d("onCreate choose prog", "Connection opened");
		
	        if (!conn.getContentType().equals("text/xml")) {
	        	toast("Error: Content-Type is not text/xml !");
	        	Log.e("onCreate choose tech", "Content type is '" + conn.getContentType() + "'");
	        }
	        
	        XMLProgrammesParser p = new XMLProgrammesParser(conn.getInputStream());
	        
	        Log.d("onCreate choose prog", "Created & filled prognames");
	        
	        progList.setAdapter(new ArrayAdapter<String>(
	        		this, android.R.layout.simple_list_item_1, p.programmes));
        
		} catch (IOException e) {
			toast("IO Exception");
			e.printStackTrace();
			return;
		}
    }
}