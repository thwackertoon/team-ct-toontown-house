import unittest

from tth.avatar import NamePattern

class TestNamePattern(unittest.TestCase):

    def setUp(self):
        filepath = '../' + NamePattern.NAMES_FILE_PATH
        self.namePattern = NamePattern.NamePattern(filepath)

    def test_generate_random_toon_name(self):
        print 'Generating 1,000 names...'
        for _ in xrange(1000):
            self.namePattern.generateRandomToonName('m')
        print 'Done.'

    def test_get_name_string(self):
        print 'Name Parts:', (19, 165, 56, 89)
        nameString = self.namePattern.getNameString('m', (19, 165, 56, 89))
        print 'Name String:', nameString
        self.assertEquals(len(nameString.split(' ')), 3)

if __name__ == '__main__':
    unittest.main()