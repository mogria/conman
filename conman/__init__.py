import os
from conman.cli import parse_args, print_help
from conman.repository import Repository
from conman.configuration_dir import ConfigurationDir

def get_conman_home():
    return os.path.join(os.getenv("HOME"), ".conman")

def get_configuration_dir():
    return ConfigurationDir(os.getenv("HOME"))

def get_repo(args):
    if 'machine_name' in args:
        return Repository(get_conman_home(), args['machine_name'])
    else:
        return Repository(get_conman_home())

def conman_init(args):
    repo = Repository.clone(args['git_repo'], get_conman_home(), args['machine_name'])
    confdir = get_configuration_dir()
    confdir.update_links(repo)

def conman_add(args):
    repo = get_repo(args)
    confdir = get_configuration_dir()
    for filepath in args.files:
        filename = confdir.relativate(filepath)
        if repo.is_module(args.module_name):
            repo.add_file_to_module(args.module_name, filename, filepath)
        else:
            repo.update_file_in_module(args.module_name, filename)

def conman_link(args):
    repo = get_repo(args)
    confdir = get_configuration_dir()
    confdir.relativate(args.link_location)
    repo.link_file_from_module(args.module_name, args.filename, args.link_location)
    confdir.update_links(repo)

def conman_list(args):
    repo = get_repo(args)
    for module in repo.get_modules():
        print(module)

def dispatch(args):
    routes = {
        'init': conman_init,
        'add': conman_add,
        'link': conman_link,
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
