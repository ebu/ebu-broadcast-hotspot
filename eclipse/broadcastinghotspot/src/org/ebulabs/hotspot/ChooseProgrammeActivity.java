/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import android.app.Activity;
import android.app.ProgressDialog;
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

/**
 * Activity to present the list of programmes to the user
 * @author mpb
 *
 */
public class ChooseProgrammeActivity extends Activity {
	
	ProgressDialog pd;
	
	private void toast(String t) {
		Toast.makeText(getApplicationContext(), t, Toast.LENGTH_SHORT).show();
	}
		
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.programmechoice);

        pd = new ProgressDialog(this);
        pd.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        pd.setMessage("Connecting to programme");
    }
    
    /** Called when the activity is first created. */
    @Override
    public void onResume() {
        super.onResume();
        
        /* Get programme list from daemon */
        
        HotspotApplication app = ((HotspotApplication)getApplication());
        
        URL url;
        String url_sz = app.hotspotURL + "/" + app.activeTech.name + "/programmes";
		try {
			url = new URL(url_sz);
		} catch (MalformedURLException e) {
			toast("Malformed URL '" + url_sz + "'");
			return;
		}
		
		Log.d(Utils.LOGTAG + "onCreate choose prog", "URL defined " + url_sz);
				
		ListView progList = (ListView)findViewById(R.id.programmeList);
		
		/* When the user clicks on the programme, fetch the associated programme data, and
		 * then call the activity to play it */
		progList.setOnItemClickListener(new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				
				Log.d(Utils.LOGTAG + "onCreate choose prog", "Click on programme, creating URL for POST");
				
		        pd.show();
				
				URL url;
				HotspotApplication app = ((HotspotApplication)getApplication());
				String url_sz = app.hotspotURL + "/" + app.activeTech.name + "/programme";
				try {
					url = new URL(url_sz);
				} catch (MalformedURLException e) {
					toast("Malformed URL '" + url_sz + "'");
					return;
				}
				
				toast("Setting programme");
				String prog = ((TextView) view).getText().toString();
				
				Log.d(Utils.LOGTAG + "onCreate choose prog", "Doing POST");
				try {
					Utils.httpPost(url_sz, prog);
				} catch (HotspotException e1) {
					toast("Setting programme failed!");
					e1.printStackTrace();
					return;
				}
				Log.d(Utils.LOGTAG + "onCreate choose prog", "Program set");
				
				
				// Fetch info
				
				URLConnection conn;
				try {
					
					conn = url.openConnection();
					
					Log.d(Utils.LOGTAG + "choose prog", "Fetch info, saving into app");
				
			        if (!conn.getContentType().equals("text/xml")) {
			        	toast("Error: Content-Type is not text/xml !");
			        	Log.e(Utils.LOGTAG + "choose prog", "Content type is '" + conn.getContentType() + "'");
			        }
			        
			        try {
						XMLProgrammeInfoParser p = new XMLProgrammeInfoParser(conn.getInputStream());
						Log.d(Utils.LOGTAG + "choose prog", "Info XML parsed");
						
						
						((HotspotApplication)getApplication()).pi = p.pi;
						Log.d(Utils.LOGTAG + "choose prog", "pi set in application, starting Activity 'play'");
						
						startActivity(new Intent("org.ebulabs.hotspot.PLAY_PROGRAMME"));
						
						
					} catch (HotspotException e) {
						e.printStackTrace();
						toast("Parsing XML Info failed");
			        	return;
					}
					
				} catch (IOException e) {
					toast("IO Exception");
					e.printStackTrace();
					return;
				}
			}
		});
		
        URLConnection conn;
		try {
			
			conn = url.openConnection();
			
			Log.d(Utils.LOGTAG + "onCreate choose prog", "Connection opened");
			
			
			if (conn.getContentType() == null) {
				toast("No answer from hotspot !");
				return;
			}
		
	        if (!conn.getContentType().equals("text/xml")) {
	        	toast("Error: Content-Type is not text/xml !");
	        	Log.e(Utils.LOGTAG + "onCreate choose prog", "Content type is '" + conn.getContentType() + "'");
	        }
	        
	        XMLProgrammesParser p = new XMLProgrammesParser(conn.getInputStream());
	        
	        Log.d(Utils.LOGTAG + "onCreate choose prog", "Created & filled prognames");
	        
	        progList.setAdapter(new ArrayAdapter<String>(
	        		this, android.R.layout.simple_list_item_1, p.programmes));
        
		} catch (IOException e) {
			toast("IO Exception");
			e.printStackTrace();
			return;
		} catch (HotspotException e) {
			toast("HotspotException");
			e.printStackTrace();
			return;
		}
    }

    @Override
	protected	void onPause() {
    	super.onPause();
		pd.dismiss();
	}
}
