package org.ebulabs.hotspot;

import java.io.IOException;
import java.io.InputStream;
import java.net.*;
import java.util.Map;
import org.ebulabs.radiodns.*;
import android.app.Activity;
import android.app.ProgressDialog;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class PlayProgrammeActivity extends Activity implements RadioVisCallbacks {
	
	private MediaPlayer mediaPlayer;
	private ProgressDialog pd;
	private RadioVisDAB radioVis; 
	
	private void toast(String t) {
		Toast.makeText(getApplicationContext(), t, Toast.LENGTH_SHORT).show();
	}

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		 pd = new ProgressDialog(this);
	     pd.setProgressStyle(ProgressDialog.STYLE_SPINNER);
	     pd.setMessage("Connecting to programme");
	     
	}
	
	@Override
	public void onResume() {
		super.onResume();
		
		pd.show();

		setContentView(R.layout.playprogramme);
		TextView v = (TextView)findViewById(R.id.playText);
		HotspotApplication app = (HotspotApplication)getApplication();

		if (app.pi == null) {
			toast("App.pi is null !");
			Log.e(Utils.LOGTAG + "PlayProgrammeActivity", "app.pi null");
			return;
		}
		
		try {
			setupRadioVis(app.pi);
		} catch (RadioDNSException e1) {
			toast("Radiovis setup failed: " + e1.getMessage());
			Log.e(Utils.LOGTAG + "PlayProgrammeActivity", "Radiovis setup failed");
		}

		StringBuilder sb = new StringBuilder();
		sb.append(app.pi.name + "\n" + app.pi.url + "\n\n");
		Map<String,String> info = app.pi.getInfo();

		for (Map.Entry<String, String> e : info.entrySet()) {
			sb.append(e.getKey() + ": " + e.getValue() + "\n");
		}
		
		v.setText(sb.toString());
				
		this.mediaPlayer = new MediaPlayer();
		/*TODO enable
		try {
			Log.d(Utils.LOGTAG + "PlayProgrammeActivity", "startAudioStream");
			
			//Utils.startAudioStream(this.mediaPlayer, app.pi.url);
		} catch (HotspotException e) {
			toast("App.pi is null !");
		
		}*/
		pd.dismiss();
	}
	
	@Override
	public void onPause()
	{
		super.onPause();
		Utils.stopAudioStream(this.mediaPlayer);
		this.mediaPlayer.release();
		if (radioVis != null)
			radioVis.stop();
	}

	void setupRadioVis(ProgrammeInfo pi) throws RadioDNSException {
		String eid_dec = pi.getInfo().get("eid");
		String sid_dec = pi.getInfo().get("sid");
		String subchid_dec = pi.getInfo().get("subchid");
		
		if (eid_dec == null || sid_dec == null || subchid_dec == null) {
			toast("Incomplete Programme information !");
			throw new RadioDNSException("Incomplete Programme information !");
		}
		
		String ECC = "4e1"; //TODO menu entry somewhere !
		String EId = Integer.toHexString(Integer.parseInt(eid_dec));
		String SId = Integer.toHexString(Integer.parseInt(sid_dec));
		String SubCHId = "0"; // talked with M. Coinchon and M. Barroco
		
		radioVis = new RadioVisDAB(ECC, EId, SId, SubCHId, this);
		radioVis.start();
		
	}
	
	
    /* Callback methods from RadioVis */
	@Override
	public void newSHOW(String Url) {
		Log.d(Utils.LOGTAG + "PlayProgrammeActivity", "SHOW " + Url);
		setVisImage(Url);
	}
	
	ImageView imView;
	Bitmap bmImg;
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
