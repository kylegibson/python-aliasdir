import argparse
import os
import os.path

from aliases import Aliases

def get_version():
    try:
        from version import __version__ as version
    except ImportError:
        version = "dev"
    return version

def main():
    default_alias_file = os.path.expanduser("~/.aliases")
    parser = argparse.ArgumentParser(
        description="If no arguments are provided, display the available aliases"
    )
    parser.add_argument('--version', action='version', version=get_version())
    parser.add_argument("alias", default=None, nargs="?",
            help="Name of alias")
    parser.add_argument("directory", default=os.getcwd(), nargs="?",
            help="Directory to associate with alias. "
                "Default is current working directory")
    parser.add_argument("--remove", default=None, metavar="alias",
            help="Remove alias if it exists")
    parser.add_argument("--show", default=None, metavar="alias",
            help="Show the value of an alias if it exists")
    parser.add_argument("--dump-alias", action="store_true",
            help="Display a list of alias statements")
    parser.add_argument("--dump-unalias", action="store_true",
            help="Display a list of unalias statements")
    parser.add_argument("--alias-file", 
            default=default_alias_file,
            help="Default is %s" % default_alias_file)
    args = parser.parse_args()

    Aliases.FILE = args.alias_file

    if args.show:
        try:
            print Aliases[args.show]
        except KeyError:
            print "Error: Alias '%s' does not exist" % args.show
    elif args.remove:
        try:
            del Aliases[args.remove]
        except KeyError:
            print "Error: Alias '%s' does not exist" % args.remove
    elif args.alias:
        Aliases[args.alias] = args.directory
    elif args.dump_unalias:
        for alias in sorted(Aliases.aliases.items()):
            print "unalias %s;" % Aliases.quote(alias[0])
    elif args.dump_alias:
        for alias in sorted(Aliases.aliases.items()):
            print "alias %s=%s;" % (
                    Aliases.quote(alias[0]), 
                    Aliases.quote("cd %s" % alias[1]))
    else:
        for alias in sorted(Aliases.aliases.items()):
            print "%-10s" % alias[0], alias[1]

if __name__ == '__main__':
    main()
