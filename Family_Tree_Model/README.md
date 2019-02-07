This is implemeted and tested using Python 2.7.10
The folder structure of the source code:
.
├── README.md
├── __init__.py
├── app.py
├── constants.py
├── dataset.txt
├── family.py
├── parser.py
├── person.py
└── test.py

==================================================
1. How to run the app:

* Go to the folder family_relation_tree
* Run: python app.py dataset.txt

==================================================
2. How to run the unit tests:

* Pytest module is required for running the unit tests
* Go to the folder family_relation_tree
* Run: py.test test.py

==================================================
3. Sample Input/Output:

ADD_TO_FAMILY <person_1> <relation> <person_2>
GET_RELATIONSHIP <person> <relationship>
Examples:

ADD_TO_FAMILY Shan king
ADD_TO_FAMILY Anga wife of Shan
ADD_TO_FAMILY Chit son of Shan
ADD_TO_FAMILY Chika daughter of Vich
ADD_TO_FAMILY Asva husband of Satvy

GET_RELATIONSHIP Ish Father
GET_RELATIONSHIP Vich Son
GET_RELATIONSHIP Gru Spouse
GET_RELATIONSHIP Vyan Brother-In-Law
GET_RELATIONSHIP Shan Grand-Son


