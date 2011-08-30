package ebu.hotspot.mediaplayer;

import java.nio.channels.DatagramChannel;

/**
 * Receive mp2 on a UDP socket, and play it
 * 
 * @author mpb
 *
 */
public class AudioDecoder {
	
	int port = -1;
	
	/** The UDP channel. */
	private DatagramChannel chan;
	
	public AudioDecoder(int port)
	{
		this.port = port;
	}
	
	public void play() {
		
	}

}
