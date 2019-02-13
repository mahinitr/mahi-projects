from constants import *

class Person:

    def __init__(self, name):
        self.name = name
        self.o_father = None
        self.o_mother = None
        self.o_spouse = None
        self.o_children = []

    @property
    def spouse(self):
        if self.o_spouse:
            return self.o_spouse.name
        return Status.REL_NOT_FOUND

    @property
    def father(self):
        if self.o_father:
            return self.o_father.name
        return Status.REL_NOT_FOUND

    @property
    def mother(self):
        if self.o_mother:
            return self.o_mother.name
        return Status.REL_NOT_FOUND

    @property
    def brother(self):
        brothers = []
        for sibling in self.o_father.o_children:
            if sibling == self:
                continue
            if isinstance(sibling, MalePerson):
                brothers.append(sibling.name)
        return brothers if brothers else Status.REL_NOT_FOUND

    @property
    def sister(self):
        sisters = []
        for sibling in self.o_father.o_children:
            if sibling == self:
                continue
            if isinstance(sibling, FemalePerson):
                sisters.append(sibling.name)
        return sisters if sisters else Status.REL_NOT_FOUND

    @property
    def son(self):
        sons = []
        for child in self.o_children:
            if isinstance(child, MalePerson):
                sons.append(child.name)
        return sons if sons else Status.REL_NOT_FOUND

    @property
    def daughter(self):
        daughters = []
        for child in self.o_children:
            if isinstance(child, FemalePerson):
                daughters.append(child.name)
        return daughters if daughters else Status.REL_NOT_FOUND

    @property
    def children(self):
        children = []
        for child in self.o_children:
            children.append(child.name)
        return children if children else Status.REL_NOT_FOUND

    @property
    def brother_in_law(self):
        brother_in_laws = []
        if self.o_spouse and self.o_spouse.o_father:
            for sibling in self.o_spouse.o_father.o_children:
                if sibling == self.o_spouse:
                    continue
                if isinstance(sibling, MalePerson):
                    brother_in_laws.append(sibling.name)
        if self.o_father:
            for sibling in self.o_father.o_children:
                if sibling == self:
                    continue
                if isinstance(sibling, FemalePerson):
                    if sibling.o_spouse:
                        brother_in_laws.append(sibling.o_spouse.name)
        if self.o_spouse and self.o_spouse.o_father:
            for sibling in self.o_spouse.o_father.o_children:
                if sibling == self.o_spouse:
                    continue
                if isinstance(sibling, FemalePerson):
                    if sibling.o_spouse:
                        brother_in_laws.append(sibling.o_spouse.name)
        return brother_in_laws

    @property
    def sister_in_law(self):
        sister_in_laws = []
        if self.o_spouse and self.o_spouse.o_father:
            for sibling in self.o_spouse.o_father.o_children:
                if sibling == self.o_spouse:
                    continue
                if isinstance(sibling, FemalePerson):
                    sister_in_laws.append(sibling.name)
        if self.o_father:
            for sibling in self.o_father.o_children:
                if sibling == self:
                    continue
                if isinstance(sibling, MalePerson):
                    if sibling.o_spouse:
                        sister_in_laws.append(sibling.o_spouse.name)
        if self.o_spouse and self.o_spouse.o_father:
            for sibling in self.o_spouse.o_father.o_children:
                if sibling == self.o_spouse:
                    continue
                if isinstance(sibling, MalePerson):
                    if sibling.o_spouse:
                        sister_in_laws.append(sibling.o_spouse.name)
        return sister_in_laws

    @property
    def maternal_uncle(self):
        maternal_uncles = []
        o_mother = self.o_mother
        if o_mother:
            if o_mother.o_father:
                for each in o_mother.o_father.o_children:
                    if isinstance(each, MalePerson):
                        maternal_uncles.append(each.name)
            for each in o_mother.brother_in_law:
                maternal_uncles.append(each)
        return maternal_uncles if maternal_uncles else Status.REL_NOT_FOUND

    @property
    def maternal_aunt(self):
        maternal_aunts = []
        o_mother = self.o_mother
        if o_mother:
            if o_mother.o_father:
                for each in o_mother.o_father.o_children:
                    if each == o_mother:
                        continue
                    if isinstance(each, FemalePerson):
                        maternal_aunts.append(each.name)
            for each in o_mother.sister_in_law:
                maternal_aunts.append(each)
        return maternal_aunts if maternal_aunts else Status.REL_NOT_FOUND

    @property
    def paternal_uncle(self):
        paternal_uncle = []
        o_father = self.o_father
        if o_father:
            if o_father.o_father:
                for each in o_father.o_father.o_children:
                    if each == o_father:
                        continue
                    if isinstance(each, MalePerson):
                        paternal_uncle.append(each.name)
            for each in o_father.brother_in_law:
                paternal_uncle.append(each)
        return paternal_uncle if paternal_uncle else Status.REL_NOT_FOUND

    @property
    def paternal_aunt(self):
        paternal_aunts = []
        o_father = self.o_father
        if o_father:
            if o_father.o_father:
                for each in o_father.o_father.o_children:
                    if isinstance(each, FemalePerson):
                        paternal_aunts.append(each.name)
            for each in o_father.sister_in_law:
                paternal_aunts.append(each)
        return paternal_aunts if paternal_aunts else Status.REL_NOT_FOUND

    @property
    def cousin(self):
        cousins = []
        parents = [self.o_father, self.o_mother]
        parent_siblings = []
        for parent in parents:
            if parent and parent.o_father:
                for each in parent.o_father.o_children:
                    if each != parent:
                        parent_siblings.append(each)
        for parent_sib in parent_siblings:
            for each in parent_sib.o_children:
                cousins.append(each.name)
        return cousins if cousins else Status.REL_NOT_FOUND

    @property
    def grand_son(self):
        grand_sons = []
        for child in self.o_children:
            for each in child.o_children:
                if isinstance(each, MalePerson):
                    grand_sons.append(each.name)
        return grand_sons if grand_sons else Status.REL_NOT_FOUND

    @property
    def grand_daughter(self):
        grand_daughters = []
        for child in self.o_children:
            for each in child.o_children:
                if isinstance(each, FemalePerson):
                    grand_daughters.append(each.name)
        return grand_daughters if grand_daughters else Status.REL_NOT_FOUND

class MalePerson(Person):

    def __init__(self, *args):
        Person.__init__(self,*args)

class FemalePerson(Person):

    def __init__(self, *args):
        Person.__init__(self,*args)
