from conman.repository import Repository
import unittest
from subprocess import call
import tempfile
import shutil
import os

class TestRepositoryConstruction(unittest.TestCase):
    def setUp(self):
        self.empty_origin_repo = tempfile.mkdtemp();
        call(['git', 'init', '--quiet', self.empty_origin_repo])
        self.empty_repo  = tempfile.mkdtemp();
        _, self.file1 = tempfile.mkstemp()
        with open(self.file1, 'w') as f:
            f.write('some sample configuration\nfile')
        _, self.file2 = tempfile.mkstemp()
        with open(self.file1, 'w') as f:
            f.write('another file with some contents and\nstuff. Yeah ...\nok?')

    def tearDown(self):
        shutil.rmtree(self.empty_origin_repo)
        shutil.rmtree(self.empty_repo)
        os.remove(self.file1)
        os.remove(self.file2)

    def test_construct(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        assert os.path.isdir(self.empty_origin_repo)
        assert os.path.isdir(os.path.join(self.empty_origin_repo, "modules"))
        assert os.path.exists(os.path.join(self.empty_origin_repo, "use-modules"))

    def test_clone(self):
        repo = Repository.clone(self.empty_origin_repo, self.empty_repo, "some-other-machine")
        assert os.path.isdir(self.empty_repo)
        assert os.path.isdir(os.path.join(self.empty_repo, "modules"))

    def test_add_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('some-module')
        assert repo.is_module('some-module')

    def test_add_duplicate_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('some-module')
        with self.assertRaises(NameError):
            repo.add_module('some-module')

    def test_get_modules_empty(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        result = repo.get_modules()
        assert len(result) == 0

    def test_get_modules(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('module-x')
        assert set(repo.get_modules()) == set(['module-x'])
        assert repo.is_module('module-x')
        repo.add_module('module-y')
        assert set(repo.get_modules()) == set(['module-x', 'module-y'])
        assert repo.is_module('module-x')
        assert repo.is_module('module-y')
        repo.add_module('module-z')
        assert set(repo.get_modules()) == set(['module-x', 'module-y', 'module-z'])
        assert repo.is_module('module-x')
        assert repo.is_module('module-y')
        assert repo.is_module('module-z')

    def test_check_have_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        with self.assertRaises(NameError):
            repo._Repository__check_have_module('inexistent-module')

    def test_check_have_file_in_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('module-z')
        with self.assertRaises(NameError):
            repo._Repository__check_have_file_in_module('module-z', 'inexistent-module')

        with self.assertRaises(NameError):
            repo._Repository__check_have_file_in_module('module-z', 'conman-link-files')

    def test_add_file_to_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('module-x')
        assert set(repo.get_files_in_module('module-x')) == set([])
        repo.add_file_to_module('module-x', 'cfg1', self.file1)
        assert set(repo.get_files_in_module('module-x')) == set(['cfg1'])
        repo.add_file_to_module('module-x', 'subdir1/d/cfg2', self.file2)
        assert set(repo.get_files_in_module('module-x')) == set(['cfg1', 'subdir1/d/cfg2'])

    def test_link_file_from_module(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('module-x')
        repo.add_file_to_module('module-x', 'file1', self.file1)
        repo.add_file_to_module('module-x', 'd/file2', self.file2)

        with self.assertRaises(NameError):
            repo.link_file_from_module('module-x', 'inexistent-file', 'some-location')

        repo.link_file_from_module('module-x', 'file1', 'some-location')
        assert repo.get_links_in_module('module-x')['some-location'] == 'file1'

        with self.assertRaises(NameError):
            repo.link_file_from_module('module-x', 'd/file2', 'some-location')

        repo.link_file_from_module('module-x', 'd/file2', 'some-other-location')
        assert repo.get_links_in_module('module-x')['some-other-location'] == 'd/file2'

    def test_get_links(self):
        repo = Repository(self.empty_origin_repo, "some-machine")
        repo.add_module('module-x')
        repo.add_module('module-y')
        repo.add_file_to_module('module-x', 'file1', self.file1)
        repo.add_file_to_module('module-y', 'd/file2', self.file2)

        assert repo.get_links() == {}
        repo.link_file_from_module('module-x', 'file1', 'some-location')
        assert repo.get_links()['some-location'] == 'modules/module-x/file1'
        repo.link_file_from_module('module-y', 'd/file2', 'some-other-location')
        assert repo.get_links()['some-other-location'] == 'modules/module-y/d/file2'
