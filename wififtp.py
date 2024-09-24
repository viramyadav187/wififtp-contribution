# -*- coding: UTF-8 -*-
# ToolName   : WiFiFTP
# Author     : KasRoudra
# License    : MIT
# Copyright  : KasRoudra (2021-2023)
# Github     : https://github.com/KasRoudra
# Contact    : https://t.me/KasRoudra
# Description: Share files between devices connected to same wlan/wifi/hotspot/router""
# Tags       : ftp, wififtp, share-files
# 1st Commit : 18/08/2021
# Language   : Python
# Portable file/script
# If you copy open source code, consider giving credit
# Env        : #!/usr/bin/env python

"""
MIT License

Copyright (c) 2021-2023 KasRoudra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from argparse import ArgumentParser
from os import name, getcwd, getenv
from os.path import isfile, isdir, dirname
from socket import socket, error, AF_INET, SOCK_STREAM
from subprocess import run, DEVNULL
from sys import executable, stdout
from time import sleep
from re import escape
import logging

# Setting up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Color snippets
colors = {
    "black": "\033[0;30m", "red": "\033[0;31m", "bred": "\033[1;31m",
    "green": "\033[0;32m", "bgreen": "\033[1;32m", "yellow": "\033[0;33m",
    "byellow": "\033[1;33m", "blue": "\033[0;34m", "bblue": "\033[1;34m",
    "purple": "\033[0;35m", "bpurple": "\033[1;35m", "cyan": "\033[0;36m",
    "bcyan": "\033[1;36m", "white": "\033[0;37m", "nc": "\033[00m"
}

version = "0.2.0"
default_dir = getcwd()
default_port = 2121

banner = f"""
{colors['red']}__        ___ _____ _  _____ _____ ____  
{colors['blue']}\ \      / (_)  ___(_)|  ___|_   _|  _ \  
{colors['green']} \ \ /\ / /| | |_  | || |_    | | | |_) |
{colors['cyan']}  \ V  V / | |  _| | ||  _|   | | |  __/ 
{colors['purple']}   \_/\_/  |_|_|   |_||_|     |_| |_| 
{colors['blue']}{" "*31}[{colors['green']}v{colors['cyan']}{version[:3]}{colors['blue']}]   
{colors['cyan']}{" "*23}[{colors['blue']}By {colors['green']}KasRoudra{colors['cyan']}]{colors['nc']}
{colors['cyan']}{" "*23}[{colors['blue']} Updated By (v2.0) {colors['green']}VIRAM YADAV{colors['cyan']}]{colors['nc']}

"""

argparser = ArgumentParser()
argparser.add_argument("-p", "--port", type=int, help=f"WiFiFTP's server port [Default: {default_port}]")
argparser.add_argument("-d", "--directory", help=f"Directory where server will start [Default: {default_dir}]")
argparser.add_argument("-u", "--username", help="FTP Username [Default: None]")
argparser.add_argument("-k", "--password", help="FTP Password [Default: None]")
argparser.add_argument("-v", "--version", help="Prints version of WiFiFTP", action="store_true")
argparser.add_argument("--tls", help="Enable TLS/SSL for secure FTP [Default: False]", action="store_true")

args = argparser.parse_args()

# Conditionally import pyftpdlib modules
def import_pyftpdlib():
    try:
        from pyftpdlib.authorizers import DummyAuthorizer
        from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
        from pyftpdlib.servers import FTPServer
        return DummyAuthorizer, FTPHandler, TLS_FTPHandler, FTPServer
    except ImportError as e:
        logging.error(f"Pyftpdlib is not installed: {e}")
        install_pyftpdlib()

# Install pyftpdlib if not found
def install_pyftpdlib():
    logging.info("Installing pyftpdlib...")
    run(f"{executable} -m pip install pyftpdlib --break-system-packages", shell=True, check=True)
    logging.info("pyftpdlib installed successfully")

def is_installed(package):
    return run(f"command -v {package}", shell=True, capture_output=True).returncode == 0

def sprint(text, second=0.05):
    for line in text + '\n':
        stdout.write(line)
        stdout.flush()
        sleep(second)

def lolcat(text, slow=True, second=0.05):
    if is_installed("lolcat"):
        run(["lolcat"], input=text, text=True)
    else:
        sprint(text, second) if slow else print(text)

def show_banner():
    run(["clear", "cls"][name == "nt"], shell=True)
    lolcat(banner, second=0.01)

def get_ip():
    with socket(AF_INET, SOCK_STREAM) as connection:
        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]

def check_local():
    ip = get_ip()
    if not ip.startswith("192") and not ip.startswith("172"):
        logging.error("You are not on a local network! Please connect to a hotspot or Wi-Fi.")
        exit()

def get_path():
    while True:
        path = args.directory or input(f"Enter path (Default: {default_dir}): ").strip() or default_dir
        path = pretty_path(escape(path), rel=False)
        if isfile(path):
            return dirname(path)
        elif isdir(path):
            return path
        logging.error(f"Invalid path: {path}")

def get_port():
    while True:
        port = args.port or input(f"Enter port (Default: {default_port}): ").strip() or str(default_port)
        if port.isdigit() and 1023 < int(port) < 65536 and is_available_port(port):
            return int(port)
        logging.error(f"Invalid or occupied port: {port}")

def is_available_port(port):
    with socket(AF_INET, SOCK_STREAM) as connection:
        return connection.connect_ex(("localhost", int(port))) != 0

def ftp(path, port, tls=False):
    DummyAuthorizer, FTPHandler, TLS_FTPHandler, FTPServer = import_pyftpdlib()
    
    authorizer = DummyAuthorizer()
    handler = TLS_FTPHandler if tls else FTPHandler
    
    if args.username and args.password:
        authorizer.add_user(args.username, args.password, path, perm="elradfmw")
    else:
        authorizer.add_anonymous(path, perm="elradfmw")
    
    handler.authorizer = authorizer
    handler.certfile = "/path/to/cert.pem" if tls else None  # TLS requires a certificate
    
    server = FTPServer(("0.0.0.0", port), handler)
    logging.info(f"Starting FTP server on ftp://{get_ip()}:{port}")
    server.serve_forever()

def start_ftp():
    show_banner()
    check_local()
    path = get_path()
    port = get_port()
    ftp(path, port, tls=args.tls)

def main():
    if args.version:
        print(f"WiFiFTP version: {version}")
        return
    try:
        start_ftp()
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()

