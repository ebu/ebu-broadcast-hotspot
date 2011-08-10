package org.ebulabs.hotspot;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;

public class ChooseTechActivity extends Activity {
	
	private void toast(String t) {
		Toast.makeText(getApplicationContext(), t, Toast.LENGTH_SHORT).show();
	}
	
    /** Called when the activity is first created. */
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.techchoice);

        /* Get list of techs from daemon */
        
        URL url;
        String url_sz = getString(R.string.daemon_url) + "/capabilities";
		try {
			url = new URL(url_sz);
		} catch (MalformedURLException e) {
			toast("Malformed URL '" + url_sz + "'");
			return;
		}
		
		Log.d("onCreate choose tech", "URL defined");
		
		//ArrayAdapter<String> techListAdapter = new ArrayAdapter<String>(this, R.id.techList, )
		
		ListView techList = (ListView)findViewById(R.id.techList);
        
		techList.setOnItemClickListener(new OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view,
                int position, long id) {
            	
            	String techname = ((TextView) view).getText().toString();
            	
            	HotspotApplication app = (HotspotApplication)getApplication();
            	
            	for (Tech t : app.allTechs) {
     	    	   if (t.name.equals(techname)) {
     	    		   app.activeTech = t;
     	    		   break;
     	    	   }
     	        }
            	
            	 
            	
            	startActivity(new Intent("org.ebulabs.hotspot.CHOOSE_PROGRAMME"));
            }
          });
		
        URLConnection conn;
		try {
			
			conn = url.openConnection();
			
			Log.d("onCreate choose tech", "Connection opened");
		
	        if (!conn.getContentType().equals("text/xml")) {
	        	toast("Error: Content-Type is not text/xml !");
	        	Log.e("onCreate choose tech", "Content type is '" + conn.getContentType() + "'");
	        }
	        
	        XMLCapabilitiesParser p = new XMLCapabilitiesParser(conn.getInputStream());

	        Log.d("onCreate choose tech", "Parsed");
				        
			ArrayList<String> technames = new ArrayList<String>();
			
			((HotspotApplication)getApplication()).allTechs = p.techs;
			
	        for (Tech t : p.techs) {
	    	   technames.add(t.name);
	        }
	        
	        Log.d("onCreate choose tech", "Created & filled technames");
	        
	        techList.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, technames));
        
		} catch (IOException e) {
			toast("IO Exception");
			e.printStackTrace();
			return;
		}
    }
}