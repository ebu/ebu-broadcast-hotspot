package org.ebulabs.hotspot;

import java.io.IOException;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.UnknownHostException;

import javax.jmdns.*;
import javax.jmdns.impl.*;

import android.util.Log;

/** Finds the hotspot using Zeroconf */
public class DiscoverHotspot {
	
	ServiceInfo info;
	
	public DiscoverHotspot() {
		
		Log.e(Utils.LOGTAG + ".DiscoverHotspot", "start");
		
		class HotspotListener implements ServiceListener
		{
			@Override
			public void serviceAdded(ServiceEvent event) {
				Log.i(Utils.LOGTAG + ".DiscoverHotspot", "serviceAdded");
			}
			
			@Override
			public void serviceRemoved(ServiceEvent event) {
				Log.i(Utils.LOGTAG + ".DiscoverHotspot", "serviceRemoved");
			}
			
			@Override
			public void serviceResolved(ServiceEvent event) {
				Log.i(Utils.LOGTAG + ".DiscoverHotspot", "serviceResolved");
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", event.getInfo().getDomain());
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", event.getInfo().getServer());
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", Integer.toString(event.getInfo().getPort()));
				
				saveHotspotLocation(event.getInfo());
			}
		}

		JmDNS jmdns;
		
		try {
			
			
			jmdns = JmDNS.create();
			
			ServiceInfo info = jmdns.getServiceInfo("_bhcp._tcp.local.", "EBU Broadcast Hotspot", 1000);
			
			
			if (info != null) {
				for (Inet4Address a : info.getInet4Addresses()) {
					Log.d(Utils.LOGTAG + ".DiscoverHotspot", "addr: " + a.toString());
				}
				for (String a : info.getURLs()) {
					Log.d(Utils.LOGTAG + ".DiscoverHotspot", "addr: " + a);
				}
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", info.getServer());
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", Integer.toString(info.getPort()));
				saveHotspotLocation(info);
			} else {
				Log.e(Utils.LOGTAG + ".DiscoverHotspot", "No mDNS response");
			} 
				 
			Log.d(Utils.LOGTAG + ".DiscoverHotspot", "addServiceListener");
			jmdns.addServiceListener("_bhcp._tcp.local.", new HotspotListener());
		} catch (Exception e) {
			Log.e(Utils.LOGTAG + ".DiscoverHotspot", "jmdns failed");
			e.printStackTrace();
		} 
		
	}
	
	private void saveHotspotLocation(ServiceInfo info) {
		this.info = info;
	}

	public String getHotspotLocation() {
		String ret = null;

		if (this.info != null) {
			
			Log.d(Utils.LOGTAG + ".DiscoverHotspot", "Inet4adlist");
			for (Inet4Address a : info.getInet4Addresses()) {
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", "Inet4ad " + a.toString());
			}
			
			Inet4Address[] addrs = info.getInet4Addresses();
			if (addrs.length > 0)
				ret = "http:/" + addrs[0].toString() + ":" + Integer.toString(info.getPort());
		}

		return ret;
	}

}



