package transaction_analyser;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

class Transaction{
	String tr_id;
	long tr_date;
	float tr_value;
	
	Transaction(String tr_id, long tr_date, float tr_value){
		this.tr_id = tr_id;
		this.tr_date = tr_date;
		this.tr_value = tr_value;
	}
}

class MerchantData{
	List<Long> tr_dates;
	List<String> tr_ids;
	List<Float> tr_values;
	int size;
	
	MerchantData(){
		tr_ids = new LinkedList<String>();
		tr_dates = new ArrayList<Long>();
		tr_values = new ArrayList<Float>();
	}
	
	void insert_transaction(Transaction tr) {
		//System.out.println("Inserting - " + tr.tr_id);
		tr_ids.add(tr.tr_id);
		tr_dates.add(tr.tr_date);
		tr_values.add(tr.tr_value);
		size++;
	}
	
	void remove_transaction(String tr_id) {
		//System.out.println("Deleting - " + tr_id);
		int pos = tr_ids.indexOf(tr_id);
		tr_ids.remove(pos);
		tr_dates.remove(pos);
		tr_values.remove(pos);
		size--;
	}
	
	void print_reports(long from, long to) {
		int count = 0;
		float total_value = 0;
		float average_value = 0;
		//System.out.println(from);
		//System.out.println(to);
		for(int i=0; i < size; i++) {
			long dt = tr_dates.get(i);
			float val = tr_values.get(i);
			//System.out.print(dt + " - " + val + ",");
			
			if( dt < from)
				continue;
			if(dt > to)
				break;
			count++;
			total_value = total_value + val;
			
		}
		if(count != 0)
			average_value = total_value / count;
		System.out.println("\nINFO: Reports: \n     Total no of transactions - " + count + "; \n     Average Transaction value - " + average_value);
	}
	
	void print_data() {
		for(int i=0; i < size; i++) {
			System.out.println(tr_ids.get(i) + "," + tr_dates.get(i) + "," + tr_values.get(i));
		}
	}
	
}

public class TransactionData {
	private Map<String, MerchantData> merchant_to_trans;
	
	public TransactionData(){
		merchant_to_trans = new TreeMap<String, MerchantData>();
	}
	
	final SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy hh:mm:ss");
	
	public boolean load_transactin(String[] values) {
		try {
			if(values.length < 5) {
				System.out.println("ERROR: Invalid format of the data in the line - " + String.join(",", values));
				return false;
			}
			//System.out.println(String.join(",", values));
			String tr_id = values[0].strip();
			long tr_date = dateFormat.parse(values[1].strip()).getTime() / 1000;
			float tr_value = Float.parseFloat(values[2].strip());
			String merchant_name = values[3].strip();
			String tr_type = values[4].strip();
			String related_tr_id = null;
			
			MerchantData merchant_data = null;
			if(merchant_to_trans.containsKey(merchant_name)) {
				merchant_data = merchant_to_trans.get(merchant_name);
			}else {
				merchant_data = new MerchantData();
				merchant_to_trans.put(merchant_name, merchant_data);
			}
			
			if(values.length != 6) {
				Transaction tr = new Transaction(tr_id, tr_date, tr_value);
				merchant_data.insert_transaction(tr);
			}
			else {
				// remove the transaction with id as related_tr_id
				related_tr_id = values[5].strip();
				merchant_data.remove_transaction(related_tr_id);
			}
			return true;
		}
		catch(Exception e) {
			System.out.println("ERROR: Failed to load transaction - " + String.join(",", values) + ". Error" + e.getMessage() );
			//e.printStackTrace();
			return false;
		}
	}
	
	public String[] get_merchants() {
		Set<String> merchant_names = merchant_to_trans.keySet();
		int size = merchant_names.size();
		String[] merchants = new String[size];
		Iterator<String> itr = merchant_names.iterator();
		int c = 0;
		while(itr.hasNext()) {
			merchants[c] = (String)itr.next();
			c++;
		}
		return merchants;
	}

	public void show_reports(String from, String to, String name) {
		System.out.println("INFO: *** Fecthing and Showing the reports ***");
		if(!merchant_to_trans.containsKey(name.strip())) {
			System.out.println("INFO: No Merchant data for " + name + " is found");
			return;
		}
		try {
			long fromDate = dateFormat.parse(from).getTime() / 1000;
			long toDate = dateFormat.parse(to).getTime() / 1000;
			MerchantData merchant_data = merchant_to_trans.get(name);
			merchant_data.print_reports(fromDate, toDate);
		} catch (ParseException e) {
			//e.printStackTrace();
			System.out.println("ERROR: Failed to parse the input values: " + e.getMessage());
		}
	}
	
}
