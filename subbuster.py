import sys
import os
import getopt
from bs4 import BeautifulSoup
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils.colors import *
from utils.request_handler import RequestHandler
from lib.brute import SubBrute

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

banner = """
               _____       _     ____            _            
              / ____|     | |   |  _ \          | |           
  _ __  _   _| (___  _   _| |__ | |_) |_   _ ___| |_ ___ _ __ 
 | '_ \| | | |\___ \| | | | '_ \|  _ <| | | / __| __/ _ \ '__|
 | |_) | |_| |____) | |_| | |_) | |_) | |_| \__ \ ||  __/ |   
 | .__/ \__, |_____/ \__,_|_.__/|____/ \__,_|___/\__\___|_|   
 | |     __/ |                                                
 |_|    |___/                                              0.1  

Open source tool for subdomain enumeration

Author: Johannes Schroeter - www.devwerks.net

[!] legal disclaimer: Usage of pySubBuster for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program

"""


def google_dork(url):
    request_handler = RequestHandler()
    data = request_handler.send("https://www.google.com/search?q=site:%s&num=100" % url)
    soup = BeautifulSoup(data, "lxml")
    results = set(re.findall(r"\w+\.{}".format(url.replace("http://", "")), soup.text))
    for subdomain in results:
        if "www." not in subdomain:
            output = GREEN + "%s \n" % (subdomain) + RESET
            sys.stdout.write(output)


def scan():
    version()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:", ["help", "url="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()

        elif opt in ("-u", "--url"):
            url = arg

    try:
        sys.stdout.write("Discover subdomains in Google\n")
        google_dork(url)
        sys.stdout.write("Bruteforcing subdomains\n")
        sub_brute = SubBrute(url.replace("http://", "http://{fuzz}."), BASE_DIR + "/wordlists/" + "sub.txt")
        sub_brute.brute_all()

    except KeyboardInterrupt:
        sys.stdout.write(RED)
        sys.stdout.write("Keyboard Interrupt detected. Exiting\n")
        sys.stdout.write(RESET)
        exit(42)


def version():
    sys.stdout.write(banner)


def help():
    sys.stdout.write("subbuster.py -u/--url URL\n")
    sys.stdout.write("Example: subbuster.py -u http://test.net/\n")


def main():
    scan()
    sys.exit()


if __name__ == "__main__":
    main()