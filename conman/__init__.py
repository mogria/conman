import os
from conman.cli import parse_args, print_help
from conman.repository import Repository

def get_conman_home():
    return os.path.join(os.getenv("HOME"), ".conman")

def conman_init(args):
    repo = Repository.clone(args['git-repo'], get_conman_home())

def main():
    args = parse_args()
    routes = {
        'init': conman_init
    }

    if 'command' in args and args['command'] in routes:
        command_func = routes[args['command']]
        command_func(args)
    else:
        print('error: unknown command')
        print_help()

if __name__ == "__init__":
    main()
