/*
Copyright (C) 2011 European Broadcasting Union
http://www.ebulabs.org

see LICENCE file information.
*/
package org.ebulabs.radiodns;

import org.xbill.DNS.*;

import android.util.Log;

/**
 * Class to do a DNS request for RadioDNS
 * @author barroco
 * @author mpb
 *
 */
public class RadioDNS {
	
	static final String LOG_SRC = "RadioDNS";
	
	String server;
	int port;
	
	public String getServer() { return server; }
	public int getPort() { return port; }
	
	public RadioDNS(String request) throws RadioDNSException {
		Record[] records;
		Lookup l1 = null;
		Lookup l2 = null;
		try {
			String initialreq = request + ".radiodns.org";
			l1 = new Lookup(initialreq, Type.CNAME);
			Record[] r1 = l1.run();
			Log.d(LOG_SRC, "DNS CNAME LOOKUP:" + initialreq + " (status:" + l1.getResult() + ")");

			if (r1 == null) {
				Log.e(LOG_SRC, "r1 is null");
				return;
			}
			
			String cname = "";
			if (r1.length > 0) {
				CNAMERecord r  = (CNAMERecord) r1[0];
				cname = r.getAlias().toString();
				cname = cname.substring(0, cname.length()-1);
				Log.d(LOG_SRC, "RESULT CNAME:" + r.getAlias());
			}

			String servicereq = "_radiovis._tcp." + cname;
			l2 = new Lookup(servicereq, Type.SRV);
			records = l2.run();
			Log.d(LOG_SRC, "DNS SRV LOOKUP:" + servicereq+" (status:" + l2.getResult() + ")");
			
			if (records == null) {
				Log.e(LOG_SRC, "records is null");
				return;
			}

			if (records.length > 0) {
				SRVRecord srv = (SRVRecord) records[0];
				String server = srv.getTarget().toString();
				server.substring(0, server.length()-1);		        	

				Log.d(LOG_SRC, "RESULT SRV: " + server + ":" + srv.getPort());

				this.server = server;
				this.port = srv.getPort();
			} 

		} 
		catch (Exception e) {
			Log.e(LOG_SRC, "error in constructor");
			e.printStackTrace();
			throw new RadioDNSException(e);
		}
	}

}
