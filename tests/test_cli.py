from conman import cli
import unittest

class TestCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = cli.create_parser()

    def setUp(self):
        pass

    def test_empty_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_invalid_command(self):
        with self.assertRaises(SystemExit):
            result = self.parser.parse_args(['invalidcommand'])

    def test_valid_command_no_args(self):
        for command in ['pull', 'push', 'list']:
            result = self.parser.parse_args([command])
            assert result.command == command

    def test_init(self):
        repo = 'https://asdasdasd.com/repo.git'
        machine = 'this-should-definitely-not-be-your-hostname'
        result = self.parser.parse_args(['init', repo, machine])
        assert result.command == 'init'
        assert result.git_repo == repo
        assert result.machine_name == machine

        result = self.parser.parse_args(['init', repo])
        assert result.command == 'init'
        assert result.git_repo == repo
        assert result.machine_name != machine # should be hostname of computer
    
    def test_new(self):
        module_name = 'random-module-a'
        result = self.parser.parse_args(['new', module_name])
        assert result.command == 'new'
        assert result.module_name == module_name
    
    def test_add(self):
        module_name = 'random-module-b'
        files = ['file123', 'qwerty']
        result = self.parser.parse_args(['add', module_name] + files)
        assert result.command == 'add'
        assert result.module_name == module_name
        assert result.files == files

    def test_link(self):
        module_name = 'random-module-c'
        filename = 'somefile'
        link_location = 'some_link_file'
        result = self.parser.parse_args(['add', module_name, filename, link_location])
        assert result.command == 'add'
        assert result.module_name == module_name
        assert result.file == filename
        assert result.link_location == link_location



if __name__ == '__main__':
    unittest.main()
