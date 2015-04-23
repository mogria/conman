from git import Repo, Actor
import os
import shutil

class Repository(object):

    LINK_FILES_NAME = "conman-link-files"
    MODULES_DIR = "modules"
    USE_MODULES_FILE = "use-modules"

    def __init__(self, directory, machine = None):
        """Create an instance by using a local repository"""
        self.directory = directory
        self.git_repo = Repo(directory)

        if machine != None:
            self.machine = machine
            self.branch = 'machine-' + machine
        else:
            self.branch = self.git_repo.active_branch.name
            if self.branch.find('machine-') == 0:
                offset = len('machine-') + 1
                self.machine = self.branch[offset:]
            else:
                self.branch = 'master'
                self.machine = 'master'

        self.actor = Actor('conman', 'conman@' + machine)

        # make sure the repo looks nice ;-)
        self.__conmanify()

    def clone(remote_url, directory, machine):
        """Create an instance by using a remote repository"""
        Repo.clone_from(remote_url, directory)
        return Repository(directory, machine)

    def get_modules(self):
        """Returns a list of all the module names"""
        trees = (self.git_repo.tree() / self.MODULES_DIR).trees
        return [item.name for item in trees]

    def add_module(self, name):
        """Adds a module"""
        if self.is_module(name):
            raise NameError('module named `' + name + '` already exists')
        module_dir = self.get_module_directory(name)
        Repository.__createfile(os.path.join(module_dir, self.LINK_FILES_NAME))
        self.__commit('add module directory for `' + name + '`', [module_dir])

    def is_module(self, name):
        """Returns a boolean wheter a module exists"""
        return name in self.get_modules()

    def __check_have_module(self, module):
        """Raises a NameError if the given module doesn't exist"""
        if not self.is_module(module):
            raise NameError('no module named `' + module + '`')

    def __check_have_file_in_module(self, module, filename):
        """Raises a NameError if the given module doesn't contain the given file"""
        if not filename in self.get_files_in_module(module):
            raise NameError('no file with the given name (`' + filename + '`) in module `' + module + '`')

    def add_file_to_module(self, module, filename, filepath):
        """Adds a file to a module.

        filename is relative to the module folder.
        filepath a file which gets copied into the module.
        """ 
        self.__check_have_module(module)
        module_dir = self.get_module_directory(module)
        dest_file = os.path.join(module_dir, filename)
        Repository.__createfile(dest_file)
        shutil.copyfile(filepath, dest_file)
        if filename in self.get_files_in_module(module):
            self.update_file_in_repository(module, filename)
        self.__commit('add file `' + filename + '` in module `' + module +'`', [dest_file])

    def update_file_in_repository(self, module, filename):
        self.__check_have_module(module)
        self.__check_have_file_in_module(module, filename)
        self.__commit('update file `' + filename + '` in module `' + module +'`', [self.get_filepath(module, filename)])

    def get_files_in_module(self, module):
        """lists all the files in a module which are already committed"""
        self.__check_have_module(module)
        module_tree = (self.git_repo.tree() / self.MODULES_DIR / module)
        files = []
        for item in module_tree.traverse():
            if item.type == 'blob':
                cut_module_dir_at = len(module_tree.path) + 1
                filename = item.path[cut_module_dir_at:]
                if filename != self.LINK_FILES_NAME:
                    files.append(filename)

        return files

    def get_links_in_module(self, module):
        self.__check_have_module(module)
        module_dir = self.get_module_directory(module)
        link_files = os.path.join(module_dir, self.LINK_FILES_NAME)
        with open(link_files, 'r') as f:
            data = f.read()
            return dict([line.split(':') for line in data.split()])

    def get_links(self):
        result = {}
        for module in self.get_modules():
            links = self.get_links_in_module(module)
            links = dict([[key, os.path.join(self.MODULES_DIR, module, links[key])] for key in links])
            result.update(links)
        return result

    def link_file_from_module(self, module, filename, linkpath):
        """Adds an entry to the modules link file."""
        self.__check_have_module(module)
        self.__check_have_file_in_module(module, filename)

        if linkpath in self.get_links():
            raise NameError('some other file already links to the exact same location')

        module_dir = self.get_module_directory(module)
        link_files = os.path.join(module_dir, self.LINK_FILES_NAME)
        with open(link_files, 'a') as f:
            f.write(linkpath + ':' + filename + '\n')
        self.__commit('add link `' + linkpath + '` to file `' + filename + '` in module `' + module + '`', [link_files])
        
    def get_module_directory(self, name):
        """Returns the full directory to a module"""
        return os.path.join(self.directory, self.MODULES_DIR, name)

    def get_filepath(self, module, filename):
        """Returns the path to a file by its module and filename"""
        module_dir = self.get_module_directory(module)
        return os.path.join(module_dir, filename)

    def __create_modules_directory(self):
        modules_directory = os.path.join(self.directory, self.MODULES_DIR)
        Repository.__createdir(modules_directory)
        self.__commit('initialized conman `modules/` directory', [modules_directory])

    def __create_machine_file(self):
        use_modules_file = os.path.join(self.directory, self.USE_MODULES_FILE)
        Repository.__createfile(use_modules_file)
        self.__commit('create use-module file for machine `' + self.machine + '`', [use_modules_file])

    def __conmanify(self):
        """Make sure all the needed directories and files are in the repository"""
        if len(self.git_repo.heads) == 0:
            self.__create_modules_directory()

        if not self.MODULES_DIR in self.git_repo.tree().trees:
            self.__create_modules_directory();

        if not self.branch in self.git_repo.heads:
            self.git_repo.create_head(self.branch, 'master')

        self.git_repo.head.reference = self.git_repo.heads[self.branch]
        self.git_repo.head.reset(index=True, working_tree=True)

        if not self.USE_MODULES_FILE in self.git_repo.tree().blobs:
            self.__create_machine_file()

    def __commit(self, message, files):
        """Add files and create a commit"""
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
