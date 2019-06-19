import argparse
import json

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='role')
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('-c', type=argparse.FileType('r'), metavar='CONF_FILE')
client_parser = subparsers.add_parser('client', parents=[_parser])
server_parser = subparsers.add_parser('server', parents=[_parser])

if __name__ == "__main__":
    args = parser.parse_args()
    if args.c is not None:
        print(json.load(args.c))
