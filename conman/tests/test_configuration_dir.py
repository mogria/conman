from conman.configuration_dir import ConfigurationDir
import unittest

class TestConfigurationDir(unittest.TestCase):
    def setUp(self):
        self.dir1 = ConfigurationDir('/some/random/directory')
        self.dir2 = ConfigurationDir('../')

    def tearDown(self):
        pass

    def test_relativate_fail(self):
        assert '1' == self.dir1.relativate('/some/random/directory/1/')
        assert '1/2/3' == self.dir1.relativate('/some/random/directory/1/2/3')
        assert '1/2' == self.dir2.relativate('../1/2/')
        assert '1/2/3' == self.dir2.relativate('../1/2/3/')

    def test_relativate_outside(self):
        with self.assertRaises(ValueError):
            self.dir1.relativate('/some/random/directory-1/1/')

