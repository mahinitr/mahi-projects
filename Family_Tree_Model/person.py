

class Person:

    def __init__(self, name):
        self.name = name
        self.father = None
        self.mother = None
        self.spouse = None
        self.children = []

    def set_spouse(self, spouse):
        self.spouse = spouse

    def get_spouse(self):
        return spouse

class MalePerson(Person):

    def __init__(self, *args):
        Person.__init__(self,*args)

class FemalePerson(Person):

    def __init__(self, *args):
        Person.__init__(self,*args)
