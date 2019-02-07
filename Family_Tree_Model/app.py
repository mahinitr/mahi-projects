import os
import sys
from family import FamilyTree
from constants import Status, Pattern
from parser import InputParser

class App:

    def __init__(self):
        self.family_tree = FamilyTree()

    def addToFamily(self, line):
        try:
            parsed = InputParser.parse_line(line)
            name1 = parsed[0]
            relation = parsed[1]
            gender = parsed[2]
            name2 = None
            if parsed[3]:
                name2 = parsed[3]
            if self.family_tree.addToFamily(name1, relation, gender, name2):
                return Status.ADD_SUCCESS
            else:
                return Status.ADD_FAILED
        except Exception as e:
            return Status.EXCEPTION + str(e)

    def getRelation(self, person, relation):
        res = self.family_tree.fetch_relatives(person, relation)
        if type(res) == list:
            res = " ".join(res)
        if len(res) == 0:
            res = Status.REL_NOT_FOUND
        return res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Provide the input file"
        sys.exit(0)
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print "Provide valid input file"
        sys.exit(0)
    app = App()
    with open(input_file) as fp:
        for line in fp.readlines():
            if line.startswith(Pattern.ADD):
                in_line = line[len(Pattern.ADD):]
                print app.addToFamily(in_line.strip())
            elif line.startswith(Pattern.GET):
                out_line = line[len(Pattern.GET):].strip()
                splitted = out_line.split(" ")
                print app.getRelation(splitted[0], splitted[1])
            elif line.strip() == "":
                continue
            else:
                print "Invalid Input"
