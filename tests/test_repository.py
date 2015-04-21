from conman.repository import Repository
import unittest
from subprocess import call
import tempfile
import os

class TestRepositoryConstruction(unittest.TestCase):
    def setUp(self):
        self.empty_origin_repo = tempfile.mkdtemp();
        call(['git', 'init', '--quiet', self.empty_origin_repo])
        self.empty_repo  = tempfile.mkdtemp();

    def tearDown(self):
        call(['rm', '-rf', self.empty_origin_repo, self.empty_repo])

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


