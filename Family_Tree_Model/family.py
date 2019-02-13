from constants import *
from person import Person, MalePerson, FemalePerson

class FamilyTree:

    def __init__(self):
        self.persons = {}
        self.root = None

    def addToFamily(self, name1, relation, gender, name2=None):
        person = None
        try:
            if name1 in self.persons:
                print "Already added this persons to family"
                return False

            if relation == KING:
                person = MalePerson(name1)
                self.root = person
                return True

            if relation in [Relation.WIFE, Relation.HUSBAND]:
                if name2 not in self.persons:
                    print "Spouse not found in the family tree"
                    return False
                if relation == Relation.WIFE:
                    person = FemalePerson(name1)
                else:
                    person = MalePerson(name1)
                o_spouse = self.persons[name2]
                o_spouse.o_spouse = person
                person.o_spouse = o_spouse
                return True

            if relation in [Relation.SON, Relation.DAUGHTER]:
                if name2 not in self.persons:
                    print "Parent not found in the family tree"
                    return False
                if relation == Relation.SON:
                    person = MalePerson(name1)
                else:
                    person = FemalePerson(name1)
                parent = self.persons[name2]
                parent.o_children.append(person)
                parent.o_spouse.o_children.append(person)
                if isinstance(parent, MalePerson):
                    person.o_father = parent
                    person.o_mother = parent.o_spouse
                else:
                    person.o_father = parent.o_spouse
                    person.o_mother = parent
                return True
            print "This relation is not supported in the system - ", relation
        finally:
            if person:
                self.persons[name1] = person

    def fetch_relatives(self, name, relation):
        if name not in self.persons:
            print "Not found in the family"
            return Status.NOT_FOUND

        relation = relation.lower()
        person = self.persons[name]
        if hasattr(person, relation):
            result = getattr(person, relation)
            return result if result else Status.REL_NOT_FOUND
        return Status.NOT_SUPPORTED

