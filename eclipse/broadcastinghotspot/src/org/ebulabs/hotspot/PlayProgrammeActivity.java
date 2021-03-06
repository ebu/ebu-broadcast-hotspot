/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.hotspot;

import java.io.IOException;
import java.net.*;
import java.util.Map;
import org.ebulabs.radiodns.*;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

/**
 * This activity plays the audio chosen, and shows the RadioVIS picture.
 * @author mpb
 *
 */
public class PlayProgrammeActivity extends Activity implements RadioVisCallbacks {
	
	private MediaPlayer mediaPlayer;
	private ProgressDialog pd;
	private RadioVisDAB radioVis;
	
	private String linkUrl;
	
	private void toast(String t) {
		Toast.makeText(getApplicationContext(), t, Toast.LENGTH_SHORT).show();
	}

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.playprogramme);
		
		linkUrl = "";

		pd = new ProgressDialog(this);
		pd.setProgressStyle(ProgressDialog.STYLE_SPINNER);
		pd.setMessage("Connecting to programme");

		ImageView imView = (ImageView)findViewById(R.id.visView);
		imView.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				if (linkUrl != null && !linkUrl.equals("")) {
					Intent i = new Intent(Intent.ACTION_VIEW);
					i.setData(Uri.parse(linkUrl));
					startActivity(i);
				}
				else {
					toast("Image link url: incorrect format");
				}

			}
		});
	}

	@Override
	public void onResume() {
		super.onResume();
		
		pd.show();

		// Show some stuff on the textview
		TextView v = (TextView)findViewById(R.id.playText);
		HotspotApplication app = (HotspotApplication)getApplication();

		if (app.pi == null) {
			toast("App.pi is null !");
			Log.e(Utils.LOGTAG + "PlayProgrammeActivity", "app.pi null");
			return;
		}
		
		StringBuilder sb = new StringBuilder();
		sb.append(app.pi.name + "\n" + app.pi.url + "\n\n");
		Map<String,String> info = app.pi.getInfo();

		for (Map.Entry<String, String> e : info.entrySet()) {
			sb.append(e.getKey() + ": " + e.getValue() + "\n");
		}
		
		v.setText(sb.toString());
		
		// Then start the player if required.
				
		if (app.enableAudio) {
			this.mediaPlayer = new MediaPlayer();
			
			try {
				Log.d(Utils.LOGTAG + "PlayProgrammeActivity", "startAudioStream");
				
				Utils.startAudioStream(this.mediaPlayer, app.pi.url);
			} catch (HotspotException e) {
				toast("startAudioStream failed !");	
			}
		}
		pd.dismiss();
		
		try {
			setupRadioVis(app.pi);
		} catch (RadioDNSException e1) {
			toast("Radiovis setup failed: " + e1.getMessage());
			Log.e(Utils.LOGTAG + "PlayProgrammeActivity", "Radiovis setup failed");
		}

	}
	
	/* Stop the player when leaving the activity */
	@Override
	public void onPause()
	{
		super.onPause();
		if (this.mediaPlayer != null) {
			Utils.stopAudioStream(this.mediaPlayer);
			this.mediaPlayer.release();
		}
		if (radioVis != null)
			radioVis.stop();
	}

	/**
	 * Reformat the programme info data and start a radiovis receiver.
	 * 
	 * @param pi
	 * @throws RadioDNSException
	 */
	void setupRadioVis(ProgrammeInfo pi) throws RadioDNSException {
		String eid_dec = pi.getInfo().get("eid");
		String sid_dec = pi.getInfo().get("sid");
		String subchid_dec = pi.getInfo().get("subchid");
		
		if (eid_dec == null || sid_dec == null || subchid_dec == null) {
			toast("Incomplete Programme information !");
			throw new RadioDNSException("Incomplete Programme information !");
		}
		
		HotspotApplication app = (HotspotApplication)getApplication();
		if (app.ecc == null) {
			app.ecc = getString(R.string.default_ecc);
		}
		String ECC = app.ecc;
		String EId = Integer.toHexString(Integer.parseInt(eid_dec));
		String SId = Integer.toHexString(Integer.parseInt(sid_dec));
		String SubCHId = "0"; // talked with M. Coinchon and M. Barroco
		
		radioVis = new RadioVisDAB(ECC, EId, SId, SubCHId, this);
		radioVis.start();
		
	}
	
	
    /* Callback methods from RadioVis */
	@Override
	public void newSHOW(String imageUrl, String linkUrl) {
		Log.d(Utils.LOGTAG + "PlayProgrammeActivity", "SHOW: " + imageUrl);
		Log.d(Utils.LOGTAG + "PlayProgrammeActivity", "SHOW URL: " + linkUrl);
		setVisImage(imageUrl);
		this.linkUrl = linkUrl;
	}

	TextView radiodnsTextview;
	String radiodnsText;
	@Override
	public void newTEXT(String text) {
		if (text != null) {
			radiodnsTextview = (TextView)findViewById(R.id.radioDNSText);
			radiodnsText = text;
			
			imView.post(new Runnable() {
		        public void run() {
		        	radiodnsTextview.setText(radiodnsText);
		        }
		      });
		}
		else {
			toast("RadioDNS TEXT invalid");
		}
		
	}
	
	/** Handle bitmap stuff */
	
	ImageView imView;
	Bitmap bmImg;
	/**
	 * Fetch a picture from the given url and show it on the imView
	 * @param url
	 */
	void setVisImage(String url) {
		URL myUrl = null;
		
		try {
			myUrl = new URL(url);
		} 
		catch (MalformedURLException e) {
			e.printStackTrace();
		}
		
		try {
			bmImg = BitmapFactory.decodeStream(myUrl.openConnection().getInputStream());
			imView = (ImageView)findViewById(R.id.visView);
			if (imView == null) 
				Log.e(Utils.LOGTAG + "PlayProgrammeActivity", "Imview is null!");
			
			// http://developer.android.com/resources/articles/painless-threading.html
			imView.post(new Runnable() {
		        public void run() {
		        	imView.setImageBitmap(bmImg);
		        }
		      });

			
		} 
		catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	
}
