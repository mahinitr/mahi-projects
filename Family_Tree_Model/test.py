import unittest
import sys
sys.path.append('..')
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
        self.assertEquals(app.getRelation("Ambi", "Grand-Grand-Son"), Status.NOT_SUPPORTED)

    def test_indirect_relations_1(self):
        app = self.app
        self.assertEquals(app.getRelation("Vyan", "Brother-In-Law"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Mina", "Brother-In-Law"), "Savya Asva")
        self.assertEquals(app.getRelation("Mina", "Sister-In-Law"), "Satvy Krpi")
        self.assertEquals(app.getRelation("Ish", "Sister-In-Law"), "Ambi Lika")
        self.assertEquals(app.getRelation("Lika", "Brother-In-Law"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Lika", "Sister-In-Law"), "Satya Ambi")
        self.assertEquals(app.getRelation("Satvy", "Sister-In-Law"), "Krpi Mina")

    def test_indirect_relations_2(self):
        app = self.app
        self.assertEquals(app.getRelation("Jata", "Maternal-Uncle"), "Vrita")
        self.assertEquals(app.getRelation("Vila", "Maternal-Uncle"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Satvy", "Maternal-Uncle"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Kriya", "Maternal-Uncle"), "Saayan Asva")
        self.assertEquals(app.getRelation("Gru", "Maternal-Uncle"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Chika", "Maternal-Aunt"), "Satya Ambi")
        self.assertEquals(app.getRelation("Lavnya", "Maternal-Aunt"), "Chika")
        self.assertEquals(app.getRelation("Driya", "Maternal-Aunt"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Vrita", "Maternal-Aunt"), "Satya Lika")
        self.assertEquals(app.getRelation("Satvy", "Paternal-Uncle"), "Ish Chit Vich")
        self.assertEquals(app.getRelation("Misa", "Paternal-Uncle"), "Savya Asva")
        self.assertEquals(app.getRelation("Vila", "Paternal-Uncle"), "Ish Chit Vyan")
        self.assertEquals(app.getRelation("Driya", "Paternal-Uncle"), "Vrita")
        self.assertEquals(app.getRelation("Drita", "Paternal-Aunt"), "Satya Lika")
        self.assertEquals(app.getRelation("Kriya", "Paternal-Aunt"), "Satvy Mina")
        self.assertEquals(app.getRelation("Mina", "Paternal-Aunt"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Lavnya", "Paternal-Aunt"), "Chika")

    def test_indirect_relations_3(self):
        app = self.app
        self.assertEquals(app.getRelation("Vila", "Cousin"), "Drita Vrita Satvy Savya Saayan")
        self.assertEquals(app.getRelation("Satvy", "Cousin"), "Drita Vrita Vila Chika")
        self.assertEquals(app.getRelation("Kriya", "Cousin"), "Misa")
        self.assertEquals(app.getRelation("Jata", "Cousin"), Status.REL_NOT_FOUND)
        self.assertEquals(app.getRelation("Vrita", "Cousin"), "Vila Chika Satvy Savya Saayan")

    def test_indirect_relations_4(self):
        app = self.app
        self.assertEquals(app.getRelation("Shan", "Grand-Son"), "Drita Vrita Vila Savya Saayan")
        self.assertEquals(app.getRelation("Shan", "Grand-Daughter"), "Chika Satvy")
        self.assertEquals(app.getRelation("Anga", "Grand-Grand-Daughter"), Status.NOT_SUPPORTED)
        self.assertEquals(app.getRelation("Anga", "Grand-Mother"), Status.NOT_SUPPORTED)
        self.assertEquals(app.getRelation("Satya", "Grand-Son"), "Kriya Misa")
        self.assertEquals(app.getRelation("Savya", "Grand-Son"), Status.REL_NOT_FOUND)


