import unittest
import sys
from app import App
from constants import Pattern, Status

input_file = "dataset.txt"

class TestFamilyTree(unittest.TestCase):

    def setUp(self):
        self.app = App()
        with open(input_file) as fp:
            for line in fp.readlines():
                if line.startswith(Pattern.ADD):
                    in_line = line[len(Pattern.ADD):]
                    print self.app.addToFamily(in_line.strip())

    def test_direct_relations(self):
        app = self.app
        self.assertEquals(app.getRelation("Ish", "Father"), "Shan")
        self.assertEquals(app.getRelation("Ish", "Mother"), "Anga")
        self.assertEquals(app.getRelation("Vich", "Father"), "Shan")
        self.assertEquals(app.getRelation("Jata", "Mother"), "Jaya")
        self.assertEquals(app.getRelation("Mnu", "Mother"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Driya", "Father"), "Drita")
        self.assertEquals(app.getRelation("Satvy", "Father"), "Vyan")
        self.assertEquals(app.getRelation("Vyan", "Father"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Vich", "Mother"), "Anga")
        self.assertEquals(app.getRelation("Chit", "Sister"), "Satya")
        self.assertEquals(app.getRelation("Savya", "Brother"), "Saayan")
        self.assertEquals(app.getRelation("Savya", "Sister"), "Satvy")
        self.assertEquals(app.getRelation("Chika", "Brother"), "Vila")
        self.assertEquals(app.getRelation("Kriya", "Spouse"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Chika", "Spouse"), "Kpila")
        self.assertEquals(app.getRelation("Shan", "Son"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Shan", "Children"), "Ish Chit Vich Satya")
        self.assertEquals(app.getRelation("Vich", "Son"), "Vila")
        self.assertEquals(app.getRelation("Jnki", "Daughter"), "Lavnya")
        self.assertEquals(app.getRelation("Satya", "Son"), "Savya Saayan")
        self.assertEquals(app.getRelation("Ambi", "Son"), "Drita Vrita")
        self.assertEquals(app.getRelation("Ambi", "Daughter"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Ambika", "Daughter"), Status.NOT_FOUND)
        self.assertEquals(app.getRelation("Ambi", "Grand_Grand_Son"), Status.NOT_SUPPORTED)

    def test_indirect_relations_1(self):
        app = self.app
        self.assertEquals(app.getRelation("Vyan", "Brother_In_Law"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Mina", "Brother_In_Law"), "Savya Asva")
        self.assertEquals(app.getRelation("Mina", "Sister_In_Law"), "Satvy Krpi")
        self.assertEquals(app.getRelation("Ish", "Sister_In_Law"), "Ambi Lika")
        self.assertEquals(app.getRelation("Lika", "Brother_In_Law"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Lika", "Sister_In_Law"), "Satya Ambi")
        self.assertEquals(app.getRelation("Satvy", "Sister_In_Law"), "Krpi Mina")

    def test_indirect_relations_2(self):
        app = self.app
        self.assertEquals(app.getRelation("Jata", "Maternal_Uncle"), "Vrita")
        self.assertEquals(app.getRelation("Vila", "Maternal_Uncle"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Satvy", "Maternal_Uncle"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Kriya", "Maternal_Uncle"), "Saayan Asva")
        self.assertEquals(app.getRelation("Gru", "Maternal_Uncle"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Chika", "Maternal_Aunt"), "Satya Ambi")
        self.assertEquals(app.getRelation("Lavnya", "Maternal_Aunt"), "Chika")
        self.assertEquals(app.getRelation("Driya", "Maternal_Aunt"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Vrita", "Maternal_Aunt"), "Satya Lika")
        self.assertEquals(app.getRelation("Satvy", "Paternal_Uncle"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Misa", "Paternal_Uncle"), "Savya Asva")
        self.assertEquals(app.getRelation("Vila", "Paternal_Uncle"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Driya", "Paternal_Uncle"), "Vrita")
        self.assertEquals(app.getRelation("Drita", "Paternal_Aunt"), "Satya Lika")
        self.assertEquals(app.getRelation("Kriya", "Paternal_Aunt"), "Satvy Mina")
        self.assertEquals(app.getRelation("Mina", "Paternal_Aunt"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Lavnya", "Paternal_Aunt"), "Chika")

    def test_indirect_relations_3(self):
        app = self.app
        self.assertEquals(app.getRelation("Vila", "Cousin"), "Drita Vrita Satvy Savya Saayan")
        self.assertEquals(app.getRelation("Satvy", "Cousin"), "Drita Vrita Vila Chika")
        self.assertEquals(app.getRelation("Kriya", "Cousin"), "Misa")
        self.assertEquals(app.getRelation("Jata", "Cousin"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Vrita", "Cousin"), "Vila Chika Satvy Savya Saayan")

    def test_indirect_relations_4(self):
        app = self.app
        self.assertEquals(app.getRelation("Shan", "Grand_Son"), "Drita Vrita Vila Savya Saayan")
        self.assertEquals(app.getRelation("Shan", "Grand_Daughter"), "Chika Satvy")
        self.assertEquals(app.getRelation("Anga", "Grand_Grand_Daughter"), Status.NOT_SUPPORTED)
        self.assertEquals(app.getRelation("Anga", "Grand_Mother"), Status.NOT_SUPPORTED)
        self.assertEquals(app.getRelation("Satya", "Grand_Son"), "Kriya Misa")
        self.assertEquals(app.getRelation("Savya", "Grand_Son"), Status.REL_NOT_FOUND)


