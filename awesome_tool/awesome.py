"""
Awesome Module to fetch Awesome People
"""
import json
import awesome

AWESOME_CONFIG = "awesome.json"

class Awesome:

    def __init__(self):
        self.awesome = []
        self.load_awesome()

    def load_awesome(self):
        with open(AWESOME_CONFIG) as fp:
            awesome_data = json.load(fp)
            awesome_people = awesome_data.get("awesome_people",[])
            for awesome_person in awesome_people:
                self.awesome.append(awesome_person)

    def get_awesome_people(self):
        return self.awesome

    def add_to_awesome_people(self, awesome_name):
        with open(AWESOME_CONFIG, "w+") as fp:
            self.awesome.append(awesome_name)
            fp.write(json.dumps({"awesome_people" : self.awesome}, indent=4))

if __name__ == "__main__":
    str_ = "Awesome()"
    eval(str_)
    print "\n *** Welcome to Awesome tool *** \n"
    awesome = Awesome()
    awesome_name = raw_input("Enter Your Name:")
    if awesome_name in awesome.get_awesome_people():
        print "\n*** Awesome Man! You are listed among the awesome people ***\n"
    else:
        awesome.add_to_awesome_people(awesome_name)
        print "\n*** Awesome Man! You are added to the list of awesome people ***\n"
