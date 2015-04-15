import os
from conman.repository import Repository

def get_conman_home():
    join(os.getenv("HOME"), ".conman")

def conman_init(args):
    repo = Repository.clone(args['git-repo'], get_conman_home)
