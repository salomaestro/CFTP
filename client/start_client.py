#!/usr/bin/env python3

from argparse import ArgumentParser
from configparser import ConfigParser

import os

from client import Client

def get_args():
    parser = ArgumentParser(description="Start up a client to connect to server.")
    parser.add_argument(
        "user",
        metavar="user",
        nargs="?",
        default="DEFAULT",
        type=str,
        help="User profile to load for connection to server."
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="file",
        type=str,
        help="File to send to server."
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List avaliable profiles"
    )

    # parse arguments
    args = parser.parse_args()

    # Find config parser
    config = ConfigParser()
    config.read("clientconfig.ini")
    
    # list user profiles
    if args.list:
        print("Defined user profiles:")
        [print(f"{entry}") for entry in config.sections()]
        exit()

    # check that given user exist
    if not args.user in config.sections() + ["DEFAULT"]:
        raise KeyError(f"User {args.user} does not exist!")

    if args.file is None:
        raise NameError(f"Filename {args.file} not found!")

    return args.user, args.file


if __name__ == "__main__":
    try:
        user, file = get_args()
    except Exception as e:
        print(e)
        exit()
    
    currPath = os.getcwd()
    client = Client(user)
    client.send_file(file, currPath)
