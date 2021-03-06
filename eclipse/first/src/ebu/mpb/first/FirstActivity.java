package ebu.mpb.first;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;

import org.xmlrpc.android.XMLRPCClient;
import org.xmlrpc.android.XMLRPCException;

import android.app.ListActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;

public class FirstActivity extends ListActivity {
	public static final int RELOAD_ID = Menu.FIRST;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        Log.w("first", "Putting foos and bars");
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, FOOS_AND_BARS));

        ListView lv = getListView();
        
        lv.setOnItemClickListener(new OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view,
                int position, long id) {
              // When clicked, show a toast with the TextView text
              Toast.makeText(getApplicationContext(), 
            		  reverseStringXMLRPC (((TextView) view).getText().toString()),
                  Toast.LENGTH_SHORT).show();
            }
          });
        
        lv.setTextFilterEnabled(true);
        
        fetchDataXMLRPC();
        
    }
    
    public boolean fetchDataXMLRPC() {
    	XMLRPCClient client;
		try {
			client = new XMLRPCClient(new URI("http://mpb.li:2720/RPC2"));
  
			Log.w("first", "got client, trying to get list");
        	Object[] r = (Object[]) client.call("get");
        	Log.w("first", "got list " + r.length);
        	
        	ArrayList<String> l = new ArrayList<String>();
        	for (int i = 0; i < r.length; i++) {
        		l.add((String) r[i]);
        		Log.w("first", "-- elem " + (String) r[i]);
        	}
        	
        	setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, l));
        	return true;
        } catch (URISyntaxException e) {
			Toast.makeText(getApplicationContext(), "URISyntaxException" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();;
		}
        catch (XMLRPCException e) {
        	Toast.makeText(getApplicationContext(), "XMLRPCException" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();
        }
        return false;
    }
    
    public String reverseStringXMLRPC(String s) {
    	XMLRPCClient client;
    	String r = "(empty)";
		try {
			client = new XMLRPCClient(new URI("http://mpb.li:2720/RPC2"));
  
			Log.w("first", "got client, trying to get reversed");
			r = (String) client.call("reverse", s);
        	Log.w("first", "got reversed " + r);
        	
        } catch (URISyntaxException e) {
			Toast.makeText(getApplicationContext(), "URISyntaxException" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();;
		}
        catch (XMLRPCException e) {
        	Toast.makeText(getApplicationContext(), "XMLRPCException" + e.getMessage(),
                    Toast.LENGTH_SHORT).show();
        }
        return r;
    }
    
    /* Create menu */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        boolean result = super.onCreateOptionsMenu(menu);
        menu.add(0, RELOAD_ID, 0, R.string.menu1);
        return result;
    }
    
    /* Define menu pressed */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case RELOAD_ID:
            fetchDataXMLRPC();
            return true;
        }
       
        return super.onOptionsItemSelected(item);
    }
    
    static final String[] FOOS_AND_BARS = new String[] {
        "Nothing"
      };
}