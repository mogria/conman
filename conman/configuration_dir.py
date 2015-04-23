import os

class ConfigurationDir(object):
    def __init__(self, directory):
        self.directory = os.path.abspath(directory) + "/"

    def relativate(self, filepath):
        filepath = os.path.abspath(filepath)
        prefix = os.path.commonprefix([self.directory, filepath])
        print(self.directory, prefix, filepath)
        if self.directory != prefix:
            raise ValueError('the file `' + filepath + '` needs to be inside `' + self.directory + '`')
        
        result = filepath[len(self.directory):]
        print(result)
        return result

    def update_links(self, repo):
        repodir = repo.directory
        links = repo.get_links()
        for link, target in links:
            update_link(os.path.join(self.directory, link), os.path.join(repodir, target))

    def update_link(self, link, target):
        if os.path.islink(link):
            print('Linking', link, 'to', target, '[exists]')
        elif os.path.isfile(link):
            print('Linking', link, 'to', target, '[file]')
        else:
            print('Linking', link, 'to', target, '[created]')
            os.symlink(link, target)

