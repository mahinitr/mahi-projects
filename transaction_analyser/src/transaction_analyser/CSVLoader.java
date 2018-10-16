package transaction_analyser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class CSVLoader {
	
	private static CSVLoader instance;
	TransactionData loadedData;
	
	private CSVLoader() {
		loadedData = new TransactionData();
	}
	
	public static CSVLoader get_instance() {
		if(instance == null) {
			instance = new CSVLoader();
		}
		return instance;
	}
	
	boolean load_csv(String file_path) {
		FileReader fr = null;
		File file = null;
		BufferedReader br = null;
		try {
			file = new File(file_path);
			fr = new FileReader(file);
			br = new BufferedReader(fr);
			String line;
			line = br.readLine(); //skip the first line
			while((line = br.readLine()) != null) {
				String[] values = line.split(",");
				loadedData.load_transactin(values);
			}
			//loadedData.query_data("Kwik-E-Mart");
			System.out.println("\nINFO: Successfully loaded the data for merchants - " + 
					String.join(", ", loadedData.get_merchants()));
			return true;
		} catch (FileNotFoundException e) {
			//e.printStackTrace();
			System.out.println("ERROR: Failed to load input csv file - " + e.getMessage());
			return false;
		} catch (IOException e) {
			//e.printStackTrace();
			System.out.println("ERROR: Failed to load input csv file - " + e.getMessage());
			return false;
		}
		catch(Exception e) {
			//e.printStackTrace();
			System.out.println("ERROR: Failed to load input csv file - " + e.getMessage());
			return false;
		}
		finally {
			try {
				if(br!=null)
					br.close();
				if(fr!=null)
					fr.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	void query_data(String from, String to, String name) {
		loadedData.show_reports(from, to, name);
	}
	
}
