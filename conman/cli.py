import os
import argparse
from socket import gethostname

parser = argparse.ArgumentParser(description='Configuration manger.')

def create_parser():
    # % conman
    subparsers = parser.add_subparsers(help='action')

    # % conman init *git_repo* [*machine-name*]
    parser_init = subparsers.add_parser('init', help='initialize conman on this machine')
    parser_init.add_argument('git_repo', help='the conman git repository to use')
    parser_init.add_argument('machine_name', nargs='?', help='name of this machine', default=gethostname())
    parser_init.set_defaults(command='init')

    # % conman new *module-name*
    parser_new = subparsers.add_parser('new', help='create a new module')
    parser_new.add_argument('module_name', help='name of the module')
    parser_new.set_defaults(command='new')

    # % conman add *module-name* *files...*
    parser_add = subparsers.add_parser('add', help='add config files to a module')
    parser_add.add_argument('module_name', help='name of the module')
    parser_add.add_argument('files', nargs='+', help='files you want to add')
    parser_add.set_defaults(command='add')
    
    # % conman link *module-name* *filepath* *link_location*
    parser_link = subparsers.add_parser('link', help='symbolically link config files')
    parser_link.add_argument('module_name', help='name of the module')
    parser_link.add_argument('filepath', help='file you want to link')
    parser_link.add_argument('link_location', help='where you want to link the file to')
    parser_link.set_defaults(command='link')

    # % conman list
    parser_list = subparsers.add_parser('list', help='list modules available')
    parser_list.set_defaults(command='list')

    # % conman push
    parser_push = subparsers.add_parser('push', help='push your modules and config to the repository')
    parser_push.set_defaults(command='push')

    # % conman pull
    parser_pull = subparsers.add_parser('pull', help='pull module and config changes from repository')
    parser_pull.set_defaults(command='pull')

    return parser

def parse_args():
    return vars(create_parser().parse_args())

def print_help():
    parser.print_help()
