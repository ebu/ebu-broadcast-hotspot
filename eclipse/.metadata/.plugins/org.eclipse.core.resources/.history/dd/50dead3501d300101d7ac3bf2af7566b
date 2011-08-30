package org.ebulabs.hotspot;

import java.net.Inet4Address;
import javax.jmdns.*;
import android.util.Log;

interface HotspotDiscoveredCallback {
	public void foundHotspotAt(String URL);
}

/** Finds the hotspot using Zeroconf */
public class DiscoverHotspot {
	
	ServiceInfo info;
	HotspotDiscoveredCallback requester;
	
	public DiscoverHotspot(HotspotDiscoveredCallback requester) {
		Log.e(Utils.LOGTAG + ".DiscoverHotspot", "start");
		
		this.requester = requester;
		
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
				
				saveAndNotifyHotspotLocation(event.getInfo());
			}
		}

		JmDNS jmdns;
		
		try {
			jmdns = JmDNS.create();
			Log.d(Utils.LOGTAG + ".DiscoverHotspot", "jmdns bound to " + jmdns.getInterface().toString());
			
			ServiceInfo info = jmdns.getServiceInfo("_bhcp._tcp.local.", "EBU_Broadcast_Hotspot", 5000);
			
			
			if (info != null) {
				for (Inet4Address a : info.getInet4Addresses()) {
					Log.d(Utils.LOGTAG + ".DiscoverHotspot", "addr: " + a.toString());
				}
				for (String a : info.getURLs()) {
					Log.d(Utils.LOGTAG + ".DiscoverHotspot", "addr: " + a);
				}
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", info.getServer());
				Log.d(Utils.LOGTAG + ".DiscoverHotspot", Integer.toString(info.getPort()));
				saveAndNotifyHotspotLocation(info);
				
				
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
	
	private void saveAndNotifyHotspotLocation(ServiceInfo info) {
		this.info = info;
		String loc = getHotspotLocation();
		Log.d(Utils.LOGTAG + ".DiscoverHotspot", "got location " + loc);
		if (loc != null)
			this.requester.foundHotspotAt(loc);
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



