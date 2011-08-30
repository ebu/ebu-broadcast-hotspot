/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.*;
import android.widget.CompoundButton.OnCheckedChangeListener;

/**
 * Some settings the user can change. Can be called from the menu in {@link ChooseTechActivity}
 * @author mpb
 *
 */
public class ConfigureActivity extends Activity {
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.configuration);
        
        CheckBox enableAudio = (CheckBox)findViewById(R.id.checkBoxAudio);
        enableAudio.setOnCheckedChangeListener(new OnCheckedChangeListener() {
			@Override
			public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
				HotspotApplication app = ((HotspotApplication)getApplication());
				app.enableAudio = isChecked;
			}
		});
    }
    
    @Override
    public void onPause() {
    	super.onPause();
    	HotspotApplication app = ((HotspotApplication)getApplication());
    	Log.d(Utils.LOGTAG + "Configure", "saving url");
    	EditText url = (EditText)findViewById(R.id.confUrl);
    	app.hotspotURL = url.getText().toString();
    	
    	EditText ecc = (EditText)findViewById(R.id.confECC);
    	app.ecc = ecc.getText().toString();
    }
    
    @Override
    public void onResume() {
    	super.onResume();
    	Log.d(Utils.LOGTAG + "onResume", "acquiring mcastlock");
    	
    	EditText urledit = (EditText)findViewById(R.id.confUrl);
    	
    	HotspotApplication app = (HotspotApplication)getApplication();
    	
		if (app.hotspotURL == null) {
			app.hotspotURL = getString(R.string.default_url);
		}
    	String url = app.hotspotURL;
    	
    	urledit.setText(url);
    	    	
    	
		if (app.ecc == null) {
			app.ecc = getString(R.string.default_ecc);
		}
		
    	EditText ecc = (EditText)findViewById(R.id.confECC);
    	
    	ecc.setText(app.ecc);
    	
    	CheckBox enableAudio = (CheckBox)findViewById(R.id.checkBoxAudio);
    	enableAudio.setChecked(app.enableAudio);
    }
}
