# Transaction Analyser Tool
### Introduction
This tool is used to analyse the the transactions of merchants and fetch the statistics.
It is built using Core Java 10 and its data structures

### How to run
1. Go to the folder src
2. Compile the java files:
    - javac transaction_analyser/*.java
3. Run command:
    - java transaction_analyser.TransactionAnalyser <CSV file path>
    - Ex: java transaction_analyser.TransactionAnalyser ../test_data/transactions.csv


### Flow of the code
1. The program execution starts with TransactionAnalyser.java's main method
2. It loads the CSV file, generates the data structures:
    - Map structure, that maps merchant name to List of its transactions(MerchantData)
    - MerchantData - with list of transaction dates, transaction ids, transaction values
    - While loading, if the payment type is reversal, then it removes the transaction with the related tr id
3. Then it asks the user for input details for reports.
4. User needs to provide the fromDate, toDate and Name of merchant.
