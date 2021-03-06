package ebu.hotspot.mediaplayer;

import java.io.IOException;

import android.app.Activity;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;


public class EBUHotspotMediaplayerActivity extends Activity {
	
	MediaPlayer mediaPlayer;
	MediaController mediaController;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
    
    public void startVideoStream() {
    	VideoView videoView = (VideoView)findViewById(R.id.videoView1);
    	
    	String url = ((EditText) findViewById(R.id.urlEntry)).getText().toString();
        		
    	videoView.setVideoURI(Uri.parse(url));
    	
    	mediaController = new MediaController(this);
    	mediaController.setMediaPlayer(videoView);
    	
    	videoView.requestFocus();
    	videoView.start();
    }
    
    public void stopAudioStream() {
    	mediaPlayer.stop();
    }
    
    public void startAudioStream() {
        
        String url = ((EditText) findViewById(R.id.urlEntry)).getText().toString();
        mediaPlayer = new MediaPlayer();
        mediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
    
        
        
        try {
			mediaPlayer.setDataSource(url);
	        mediaPlayer.prepare(); // might take long! (for buffering, etc)
		} catch (IllegalArgumentException e) {
			Toast.makeText(getApplicationContext(), "IllegalArgumentException\n" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();
		} catch (IllegalStateException e) {
			Toast.makeText(getApplicationContext(), "IllegalStateException\n" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();
		} catch (IOException e) {
			Toast.makeText(getApplicationContext(), "IOException\n" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();
		}
		
        mediaPlayer.start();
    }
    
    /* Create menu */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
    	MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main_options, menu);
        return true;
    }
    
    /* Define menu pressed */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.start_audio:
            startAudioStream();
            return true;
        case  R.id.stop_audio:
            startAudioStream();
            return true;
        case R.id.start_video:
        	startVideoStream();
        }
       
        return super.onOptionsItemSelected(item);
    }
}