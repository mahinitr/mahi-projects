# Transaction Analyser Tool
### Introduction
This tool is used to analyse the the transactions of merchants and fetch the statistics.
It is built using Core Java 10 and its data structures

### How to run
1. Go to the folder src
2. Compile the java files: javac transaction_analyser/*.java
3. Run command: java transaction_analyser.TransactionAnalyser <CSV file path>
    - Ex: java transaction_analyser.TransactionAnalyser ../test_data/transactions.csv


### Implementation Details
1. The program execution starts with TransactionAnalyser.java's main method
2. It loads the CSV file and generates the data structures
3. Then it asks the user for input details for reports.
