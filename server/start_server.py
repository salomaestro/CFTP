#!/usr/bin/env python3

from argparse import ArgumentParser
from configparser import ConfigParser

from server import Server

def get_args():
    parser = ArgumentParser(description="Start up a server ready to recive files.")
    parser.add_argument(
        "profile",
        metavar="profile",
        nargs="?",
        default="DEFAULT",
        type=str,
        help="Server profile to load on server startup"
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List avaliable profiles."
    )

    args = parser.parse_args()

    # Get config parser
    config = ConfigParser()
    config.read("serverconfig.ini")

    if args.list:
        print("Defined user profiles:")
        [print(f"{entry}") for entry in config.sections()]
        exit()

    if not args.profile in config.sections() + ["DEFAULT"]:
        raise KeyError(f"Profile {args.profile} not found!")
    
    return args.profile

if __name__ == "__main__":
    try:
        profile = get_args()
    except Exception as e:
        print(e)
        exit()
    
    server = Server(profile)
    server.run()
