import sys
from parser import InputParser
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
                spouse = self.persons[name2]
                spouse.spouse = person
                person.spouse = spouse
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
                parent.children.append(person)
                parent.spouse.children.append(person)
                if isinstance(parent, MalePerson):
                    person.father = parent
                    person.mother = parent.spouse
                else:
                    person.father = parent.spouse
                    person.mother = parent
                return True
            print "This relation is not supported in the system - ", relation
        finally:
            if person:
                self.persons[name1] = person

    @staticmethod
    def get_brother_in_laws(person):
        brother_in_laws = []
        if person.spouse and person.spouse.father:
            for sibling in person.spouse.father.children:
                if sibling == person.spouse:
                    continue
                if isinstance(sibling, MalePerson):
                    brother_in_laws.append(sibling.name)
        if person.father:
            for sibling in person.father.children:
                if sibling == person:
                    continue
                if isinstance(sibling, FemalePerson):
                    if sibling.spouse:
                        brother_in_laws.append(sibling.spouse.name)
        if person.spouse and person.spouse.father:
            for sibling in person.spouse.father.children:
                if sibling == person.spouse:
                    continue
                if isinstance(sibling, FemalePerson):
                    if sibling.spouse:
                        brother_in_laws.append(sibling.spouse.name)
        return brother_in_laws

    @staticmethod
    def get_sister_in_laws(person):
        sister_in_laws = []
        if person.spouse and person.spouse.father:
            for sibling in person.spouse.father.children:
                if sibling == person.spouse:
                    continue
                if isinstance(sibling, FemalePerson):
                    sister_in_laws.append(sibling.name)
        if person.father:
            for sibling in person.father.children:
                if sibling == person:
                    continue
                if isinstance(sibling, MalePerson):
                    if sibling.spouse:
                        sister_in_laws.append(sibling.spouse.name)
        if person.spouse and person.spouse.father:
            for sibling in person.spouse.father.children:
                if sibling == person.spouse:
                    continue
                if isinstance(sibling, MalePerson):
                    if sibling.spouse:
                        sister_in_laws.append(sibling.spouse.name)
        return sister_in_laws

    def fetch_relatives(self, name, relation):
        relation = relation.lower()
        if name not in self.persons:
            print "Not found in the family"
            return Status.NOT_FOUND
        person = self.persons[name]
        if relation == Relation.SPOUSE:
            if person.spouse:
                return person.spouse.name
            return Status.REL_NOT_FOUND
        if relation == Relation.FATHER:
            if person.father:
                return person.father.name
            return Status.REL_NOT_FOUND
        if relation == Relation.MOTHER:
            if person.mother:
                return person.mother.name
            return Status.REL_NOT_FOUND
        if relation == Relation.BROTHER:
            brothers = []
            for sibling in person.father.children:
                if sibling == person:
                    continue
                if isinstance(sibling, MalePerson):
                    brothers.append(sibling.name)
            return brothers if brothers else Status.REL_NOT_FOUND
        if relation == Relation.SISTER:
            sisters = []
            for sibling in person.father.children:
                if sibling == person:
                    continue
                if isinstance(sibling, FemalePerson):
                    sisters.append(sibling.name)
            return sisters if sisters else Status.REL_NOT_FOUND
        if relation == Relation.SON:
            sons = []
            for child in person.children:
                if isinstance(child, MalePerson):
                    sons.append(child.name)
            return sons if sons else Status.REL_NOT_FOUND
        if relation == Relation.DAUGHTER:
            daughters = []
            for child in person.children:
                if isinstance(child, FemalePerson):
                    daughters.append(child.name)
            return daughters if daughters else Status.REL_NOT_FOUND

        if relation == Relation.CHILDREN:
            children = []
            for child in person.children:
                children.append(child.name)
            return children if children else Status.REL_NOT_FOUND

        if relation == Relation.BROTHER_IN_LAW:
            res = FamilyTree.get_brother_in_laws(person)
            return res if res else Status.REL_NOT_FOUND

        if relation == Relation.SISTER_IN_LAW:
            res = FamilyTree.get_sister_in_laws(person)
            return res if res else Status.REL_NOT_FOUND

        if relation == Relation.MATERNAL_UNCLE:
            maternal_uncles = []
            mother = person.mother
            if mother:
                if mother.father:
                    for each in mother.father.children:
                        if isinstance(each, MalePerson):
                            maternal_uncles.append(each.name)
                for each in FamilyTree.get_brother_in_laws(mother):
                    maternal_uncles.append(each)
            return maternal_uncles if maternal_uncles else Status.REL_NOT_FOUND

        if relation == Relation.MATERNAL_AUNT:
            maternal_aunts = []
            mother = person.mother
            if mother:
                if mother.father:
                    for each in mother.father.children:
                        if each == mother:
                            continue
                        if isinstance(each, FemalePerson):
                            maternal_aunts.append(each.name)
                for each in FamilyTree.get_sister_in_laws(mother):
                    maternal_aunts.append(each)
            return maternal_aunts if maternal_aunts else Status.REL_NOT_FOUND

        if relation == Relation.PATERNAL_UNCLE:
            paternal_uncle = []
            father = person.father
            if father:
                if father.father:
                    for each in father.father.children:
                        if each == father:
                            continue
                        if isinstance(each, MalePerson):
                            paternal_uncle.append(each.name)
                for each in FamilyTree.get_brother_in_laws(father):
                    paternal_uncle.append(each)
            return paternal_uncle if paternal_uncle else Status.REL_NOT_FOUND

        if relation == Relation.PATERNAL_AUNT:
            paternal_aunts = []
            father = person.father
            if father:
                if father.father:
                    for each in father.father.children:
                        if isinstance(each, FemalePerson):
                            paternal_aunts.append(each.name)
                for each in FamilyTree.get_sister_in_laws(father):
                    paternal_aunts.append(each)
            return paternal_aunts if paternal_aunts else Status.REL_NOT_FOUND

        if relation == Relation.COUSIN:
            cousins = []
            parents = [person.father, person.mother]
            parent_siblings = []
            for parent in parents:
                if parent and parent.father:
                    for each in parent.father.children:
                        if each != parent:
                            parent_siblings.append(each)
            for parent_sib in parent_siblings:
                for each in parent_sib.children:
                    cousins.append(each.name)
            return cousins if cousins else Status.REL_NOT_FOUND

        if relation == Relation.GRAND_SON:
            grand_sons = []
            for child in person.children:
                for each in child.children:
                    if isinstance(each, MalePerson):
                        grand_sons.append(each.name)
            return grand_sons if grand_sons else Status.REL_NOT_FOUND

        if relation == Relation.GRAND_DAUGHTER:
            grand_daughters = []
            for child in person.children:
                for each in child.children:
                    if isinstance(each, FemalePerson):
                        grand_daughters.append(each.name)
            return grand_daughters if grand_daughters else Status.REL_NOT_FOUND

        return Status.NOT_SUPPORTED




