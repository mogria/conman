import os
from conman.cli import parse_args, print_help
from conman.repository import Repository

def get_conman_home():
    return os.path.join(os.getenv("HOME"), ".conman")

def get_repo(args):
    return Repository(get_conman_home(), args['machine_name'])

def conman_init(args):
    repo = Repository.clone(args['git_repo'], get_conman_home(), args['machine_name'])

def conman_list(args):
    repo = get_repo(args)
    repo.get_modules()

def dispatch(args):
    routes = {
        'init': conman_init,
        'list': conman_list
    }

    if 'command' in args and args['command'] in routes:
        command_func = routes[args['command']]
        command_func(args)
    else:
        print('error: unknown command')
        print_help()


def main():
    args = parse_args()
    dispatch(args)

if __name__ == "__init__":
    main()
