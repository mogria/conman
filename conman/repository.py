from git import Repo

class Repository(object):

    def __init__(self, directory):
        self.git_repo = Repo(directory)

    def clone(remote_url, directory):
        Repo.clone_from(remote_url, directory)
        return Repository(directory)

    def get_modules():
        git_repo.commit.tree
        for item in tree.traverse():
            pass
