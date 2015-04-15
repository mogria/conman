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
        self.conmanify()

    def clone(remote_url, directory, machine):
        Repo.clone_from(remote_url, directory)
        return Repository(directory, machine)

    def create_modules_folder(self):
        print('creating modules folder ...')
        index = self.git_repo.index
        modules_folder = os.path.join(self.directory, 'modules')
        if not os.path.exists(modules_folder):
            os.makedirs(modules_folder)
        modules_keep_file = os.path.join(modules_folder, '.keep')
        open(modules_keep_file, 'w').close()
        index.add([modules_keep_file])
        index.commit('initialized conman `modules/` folder', author=self.actor, committer=self.actor)

    def create_machine_file(self):
        pass

    def conmanify(self):
        if len(self.git_repo.heads) == 0:
            self.create_modules_folder()

        print(self.git_repo.tree() / 'modules')
        if not 'modules' in self.git_repo.tree().trees:
            self.create_modules_folder();

        if not self.branch in self.git_repo.heads:
            self.git_repo.create_head(self.branch, 'master')

        self.git_repo.head.reference = self.git_repo.heads[self.branch]
        self.git_repo.head.reset(index=True, working_tree=True)

        if not 'use-modules' in self.git_repo.tree().blobs:
            pass

    def get_modules(self):
        tree = self.git_repo.tree()
        for item in tree.traverse():
            print(item)
