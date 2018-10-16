/*
 * 
 * author: maheshwar
 *
 */

package transaction_analyser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class TransactionAnalyser {

	public static void main(String[] args) {
		// Pass the CSV file as input while running
		if(args.length < 1) {
			System.out.println("ERROR: Less no of arguments. CSV file is required as argument");
			return;
		}
		// args[0] is the path of the CSV file.
		// check of the file exists, load csv data into data structure
		String file_path = args[0];
		System.out.println("INFO: Input file is - " + file_path);
		CSVLoader loader = CSVLoader.get_instance();
		if(!loader.load_csv(file_path)) {
			return;
		}
		
		Scanner in = new Scanner(System.in);
		String input;
		while(true) {
			System.out.print("\nINFO: Do you want to continue to see the reports...? Yes/No: ");
			input = in.nextLine().toLowerCase();
			if(input.endsWith("yes")) {
				System.out.print("Please provide the below inputs.\n");
				System.out.print("     From Date(DD/MM/YYYY hh:mm:ss): ");
				String fromDate = in.nextLine();
				System.out.print("     To Date(DD/MM/YYYY hh:mm:ss): ");
				String toDate = in.nextLine();
				System.out.print("     Merchant Name: ");
				String merchantName = in.nextLine();
				loader.query_data(fromDate, toDate, merchantName);
			}else {
				break;
			}
		}
		System.out.println("INFO: You exited the tool");
		
	}

}
