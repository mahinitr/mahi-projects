 
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;

class DoubleValue{
	
	String readFileName(){
		String file = "";
		System.out.print("\nEnter the file name...(ex: file1.txt) - ");
		try
		{
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			file = br.readLine();
		}
		catch(IOException ioe)
		{
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}
		return file;
	}
		
	void inputDoubleValues(DataOutputStream out_){
		BufferedReader br = null;
		String input = "";
		try
		{			
			br = new BufferedReader(new InputStreamReader(System.in));
			System.out.println("\nEnter double values... type 'q' to exit ");	
			input = br.readLine();			
			while(!input.equals("q"))
			{
				double d = Double.parseDouble(input);
				out_.writeDouble(d);
				input = br.readLine();
			}
		}		
		catch(NumberFormatException ne)
		{
			System.out.println("Invalid input: " + ne);
			System.exit(0);
		}
		catch(IOException ioe)
		{
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}
	}
	
	void createFile(){
		String file = readFileName();
		while(file.trim().equals("")){
			file = readFileName();
		}
		FileOutputStream out = null;
		DataOutputStream dout = null;
		try{
			out = new FileOutputStream(file);
			dout = new DataOutputStream(out);	
			inputDoubleValues(dout);
		}
		catch(IOException ioe){
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}
		finally{
			if(out!=null){
				try{ 
					out.close();
					dout.close();
				}
				catch(IOException e){
					System.out.println("IO Error : " + e);
				}
			}				
		}
		
	}
	void searchFile(){
		String data = outputFile();
		String value = "";
		try
		{
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			System.out.println("Enter double value to search");
			value = br.readLine();
			if(data.toLowerCase().contains(value.toLowerCase())){
				System.out.println(("Found"));
			}
			else{
			System.out.println(("Not Found"));
			}
		}
		catch(IOException ioe)
		{
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}
	}
	void sortFile(){
		String data = outputFile();
		String[] arr = data.split(" ");
		java.util.Arrays.sort(arr);
		for(String s : arr){
			System.out.println(s);
		}
	}
	
	void displayFile(){
		System.out.println(outputFile());
	}
	
	String outputFile(){
		String res = new String();
		String file = readFileName();
		while(file.trim().equals("")){
			file = readFileName();
		}
		FileInputStream in = null;
		DataInputStream din = null;
		try{
			in = new FileInputStream(file);
			din = new DataInputStream(in);	
			while(din.available()>0) {
				double d = din.readDouble();
				res = res + " " + d;
				//System.out.println(d);
			}
			return res;
		}
		catch(IOException ioe){
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}
		finally{
			
				try{ 
				if(in!=null){
				in.close();}
				if(din!=null)
					din.close();
				}
				catch(IOException e){
					System.out.println("IO Error : " + e);
				}
						
		}
		return res;
	}
	
}

public class TestDV{
	
	static void displayText(){
				
		System.out.println("\n 1. Create a new file");
		System.out.println(" 2. Search for a value");
		System.out.println(" 3. Sort the values");
		System.out.println(" 4. Display values from a file");
		System.out.println(" 5. Exit\n");
	}
	
	static int readInput(){
		int input = -1;
		try
		{
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			input = Integer.parseInt(br.readLine());
		}		
		catch(NumberFormatException ne)
		{
			System.out.println("Invalid input" + ne);
			System.exit(0);
		}
		catch(IOException ioe)
		{
			System.out.println("IO Error :" + ioe);
			System.exit(0);
		}     
		return input;
	}
	
	
	public static void  main(String[] args){
		DoubleValue dv = new DoubleValue();
		System.out.println("\n****Welcome to Double Value Program...*****\n");
		TestDV.displayText();

		while(true){
			System.out.print("\nPlease choose an option: ");
			int op = TestDV.readInput();
			if(op != 1 && op != 2 && op != 3 && op != 4 && op != 5){
				System.out.print("\nInvalid option, ");
				continue;
			}
			if(op == 1){
				dv.createFile();
			}
			else if(op == 2){
				dv.searchFile();
			}
			else if(op == 3){
				dv.sortFile();
			}
			else if(op == 4){
				dv.displayFile();
			}
			else if(op == 5){			
				System.exit(0);
				break;
			}
		}		
		System.out.println("\nExiting...\n");
	}	
}