from git import Repo, Actor
import os

class Repository(object):

    def __init__(self, directory, machine):
        self.directory = directory
        self.machine = machine
        self.branch = 'machine-' + machine
        self.git_repo = Repo(directory)
        self.actor = Actor('conman', 'conman@' + machine)

        # make sure the repo looks nice ;-)
        self.__conmanify()

    def clone(remote_url, directory, machine):
        Repo.clone_from(remote_url, directory)
        return Repository(directory, machine)

    def get_modules(self):
        trees = (self.git_repo.tree() / 'modules').trees
        return [item.name for item in trees]

    def add_module(self, name):
        if self.is_module(name):
            raise NameError('module named `' + name + '` already exists')
        module_dir = self.get_module_directory(name)
        Repository.__createdir(module_dir)
        self.__commit('add module directory for `' + name + '`', [module_dir])

    def is_module(self, name):
        return name in self.get_modules()

    def get_module_directory(self, name):
        return os.path.join(self.directory, 'modules', name)

    def __create_modules_directory(self):
        modules_directory = os.path.join(self.directory, 'modules')
        Repository.__createdir(modules_directory)
        self.__commit('initialized conman `modules/` directory', [modules_directory])

    def __create_machine_file(self):
        use_modules_file = os.path.join(self.directory, 'use-modules')
        Repository.__createfile(use_modules_file)
        self.__commit('create use-module file for machine `' + self.machine + '`', [use_modules_file])

    def __conmanify(self):
        if len(self.git_repo.heads) == 0:
            self.__create_modules_directory()

        if not 'modules' in self.git_repo.tree().trees:
            self.__create_modules_directory();

        if not self.branch in self.git_repo.heads:
            self.git_repo.create_head(self.branch, 'master')

        self.git_repo.head.reference = self.git_repo.heads[self.branch]
        self.git_repo.head.reset(index=True, working_tree=True)

        if not 'use-modules' in self.git_repo.tree().blobs:
            self.__create_machine_file()

    def __commit(self, message, files):
        index = self.git_repo.index
        index.add(files)
        index.commit(message, author=self.actor, committer=self.actor)

    @staticmethod
    def __createfile(filepath):
        dirpath = os.path.dirname(filepath)
        Repository.__createdir(dirpath, False)
        open(filepath, 'w').close()

    @staticmethod
    def __createdir(dirpath, dotKeepFile=True):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        if dotKeepFile:
            keep_file = os.path.join(dirpath, '.keep')
            Repository.__createfile(keep_file)
