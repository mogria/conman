import os
import argparse
def main():
    # % conman
    parser = argparse.ArgumentParser(description='Configuration manger.')
    subparsers = parser.add_subparsers(help='action')

    # % conman init
    parser_init = subparsers.add_parser('init', help='initialize conman on this machine')
    parser_init.add_argument('git-repo', help='the conman git repository to use')
    parser_init.add_argument('machine-name', nargs='?', default=os.getenv('HOSTNAME'), help='name of this machine')

    # % conman new *module-name*
    parser_new = subparsers.add_parser('new', help='create a new module')
    parser_new.add_argument('module-name', help='name of the module')

    # % conman add *module-name*
    parser_add = subparsers.add_parser('add', help='add config files to a module')
    parser_add.add_argument('module-name', help='name of the module')
    parser_add.add_argument('files', nargs='+', help='files you want to add')
    
    # % conman link *module-name*
    parser_link = subparsers.add_parser('link', help='symbolically link config files')
    parser_link.add_argument('module-name', help='name of the module')
    parser_link.add_argument('file', help='file you want to link')
    parser_link.add_argument('link-location', help='where you want to link the file to')

    # % conman push
    parser_push = subparsers.add_parser('push', help='push your modules and config to the repository')

    # % conman pull
    parser_pull = subparsers.add_parser('pull', help='pull module and config changes from repository')

    args = parser.parse_args()

if __name__ == "__main__":
    main()
