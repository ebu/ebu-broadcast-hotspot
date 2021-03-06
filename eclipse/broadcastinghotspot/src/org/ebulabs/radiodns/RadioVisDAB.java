/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.radiodns;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.util.HashMap;

import android.util.Log;

/**
 * Radiovis for DAB.
 * 
 * Creates the DNS request, connects to the correct STOMP server, and calls the callback
 * functions when new messages arrive.
 * 
 * @author mpb
 *
 */
public class RadioVisDAB {
	
	RadioDNS visserver;
	StompConnectionHandler stomp;
	String topic;
	
	/**
	 * Create a new RadioVisDAB instance.
	 * 
	 * All parameters are hexadecimal strings (without "0x" prefix)
	 * 
	 * @param ECC Extended Country Code
	 * @param EId Ensemble Id
	 * @param SId Service Id
	 * @param SubCHId Subchannel Id
	 * @throws RadioDNSException 
	 */
	public RadioVisDAB(String ECC, String EId, String SId, String SubCHId, RadioVisCallbacks callbacks) throws RadioDNSException {
		this.visserver = new RadioDNS(SubCHId + "." + SId + "." + EId + "." + ECC + ".dab");
		
		this.topic = "/topic/dab/" + ECC + "/" + EId + "/" + SId + "/" + SubCHId;
		
		this.stomp = new StompConnectionHandler(visserver.getServer(), visserver.getPort(), callbacks, this.topic);
	}
	
	public void start() {
		this.stomp.start();
	}
	
	public void stop() {
		this.stomp.stopReceiver();
	}
}

class StompConnectionHandler extends Thread {
	Socket sock;
	RadioVisCallbacks callbacks;
	String topic;
	String server;
	int port;
	
	boolean run;
	
	Exception lastError;
	
	public StompConnectionHandler(String server, int port, RadioVisCallbacks callbacks, String topic) throws RadioDNSException {
		this.callbacks = callbacks;
		this.topic = topic;
		this.server = server;
		this.port = port;
		this.run = true;
		
	}
	
	@Override
	public void run() {
		
		try {
			sock = new Socket(server, port);
			PrintStream out = new PrintStream(sock.getOutputStream());
			InputStreamReader in = new InputStreamReader(sock.getInputStream());
			
			out.print("CONNECT\n\n\0");
			String r = receiveMessage(in);
			String rs[] = r.split("\n");
			
			if (rs.length == 0 || !rs[0].equals("CONNECTED")) {
				Log.e("RadioDNS", "Could not connect");
				throw new RadioDNSException("Did not receive correct answer from server");
			}
			
			Log.w("RadioDNS", "Subscribing to " + topic);
			out.print("SUBSCRIBE\ndestination: " + this.topic + "/image\nack: auto\n\n\0");
			out.print("SUBSCRIBE\ndestination: " + this.topic + "/text\nack: auto\n\n\0");
			
			while (this.run) {
				r = receiveMessage(in);
				Log.w("RadioDNS", "Recvd message " + r);
				
				StompMessage msg = StompMessage.parse(r);
				
				Log.d("RadioDNS", "Got message cmd " + msg.command);
				Log.d("RadioDNS", "Got message body" + msg.body);
				
				if (msg.command.equals("MESSAGE") && msg.body.startsWith("SHOW")) {
					if (msg.headers.containsKey("link")) {
						callbacks.newSHOW(msg.body.substring("SHOW ".length()), msg.headers.get("link"));
					}
					else {
						callbacks.newSHOW(msg.body.substring("SHOW ".length()), null);
					}
					
				}
				
				if (msg.command.equals("MESSAGE") && msg.body.startsWith("TEXT")) {
					callbacks.newTEXT(msg.body.substring("TEXT ".length()));
				}
			}
			Log.i("RadioDNS", "Leaving main loop");
			sock.close();
			
		} 
		catch (Exception e) {
			e.printStackTrace();
			
			this.lastError = new RadioDNSException(e);
		}
	}
	
	public void stopReceiver() {
		synchronized (this) {
			try {
				if (sock != null)
					sock.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			this.run = false;
		}
		
	}
	
	String receiveMessage(InputStreamReader in) throws RadioDNSException {
		StringBuilder sb = new StringBuilder();
		
		char[] c = new char[1];
		
		try {
			while (in.read(c) != -1) {
				if (c[0] == '\0')
					break;
				sb.append(c[0]);
			}
		}
		catch (IOException e) {
			e.printStackTrace();
			Log.e("RadioDNS", "receiveToken failed");
			throw new RadioDNSException(e);
		}
		
		return sb.toString();
	}
}

class StompMessage {
	
	String message;
	
	public String command;
	public HashMap<String, String> headers;
	public String body;
	
	@Override
	public String toString() {
		return this.message;
	}
	
	public static StompMessage parse(String in) {
		StompMessage msg = new StompMessage();
		
		Log.d("RadioDNS", "=== parse " + in);
		Log.d("RadioDNS", "=== end of parse");
		
		// Skip \n's at the begining
		int skip = 0;
		
		while (in.charAt(skip) == '\n' || in.charAt(skip) == '\r') {
			skip++;
			if (skip > in.length()) {
				return null;
			}
		}
			
		
		int i = in.indexOf('\n', skip+1);
		
		Log.d("RadioDNS", "skip = " + Integer.toString(skip) + " ; i = " + Integer.toString(i));
		
		msg.command = in.substring(skip, i);
		
		i++; // Eat the \n
		
		int j = in.indexOf("\n\n");
		
		// headers go from i to j
		
		String headers = in.substring(i, j);
		Log.d("RadioDNS", "=== headers " + headers);
		Log.d("RadioDNS", "=== end of headers");
		
		msg.headers = new HashMap<String, String>();
		
		for (String kv : headers.split("\n")) {
			String key_val[] = kv.split(":", 2);
			if (key_val.length == 2)
				msg.headers.put(key_val[0], key_val[1]);
		}
		
		if (j+2 < in.length()) {
			msg.body = in.substring(j+2, in.length());
		}
		else
		{
			msg.body = "";
		}
		Log.d("RadioDNS", "=== body " + msg.body);
		Log.d("RadioDNS", "=== end of body");
		return msg;
	}
}
