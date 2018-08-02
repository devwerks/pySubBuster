import sys
import os
import getopt
from bs4 import BeautifulSoup
import re
from dns import resolver

from utils.colors import *
from utils.progress_bar import ProgressBar
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

Python tool for subdomain enumeration

Author: Johannes Schroeter - www.devwerks.net

[!] legal disclaimer: Usage of pySubBuster for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program

"""


def uniquify(seq, idfun=None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
         marker = idfun(item)
         if marker in seen: continue
         seen[marker] = 1
         result.append(item)
    return result


def query_dns(url):
    for qtype in 'A', 'AAAA', 'MX', 'TXT', 'SOA', 'NS':
        answer = resolver.query(url.replace("http://", ""), qtype, raise_on_no_answer=False)
        if answer.rrset is not None:
            output = GREEN + "%s \n" % (answer.rrset) + RESET
            sys.stdout.write(output)


def query_search(url):

    sublist = []
    engine_urls = ['https://www.virustotal.com/en/domain/%s/information/',
                   'https://www.google.com/search?q=site:%s&num=100',
                   'https://search.yahoo.com/search?p=%s&b=1']

    i = 0
    for engine in engine_urls:
        request_handler = RequestHandler()
        data = request_handler.send(engine % url.replace("http://", ""))
        if data == 'None':
            return None
        soup = BeautifulSoup(data, "lxml")
        results = set(re.findall(r"\w+\.{}".format(url.replace("http://", "")), soup.text))
        for subdomain in results:
            if "www." not in subdomain:
                output = GREEN + "%s\n" % (subdomain) + RESET
                sublist.append(output)
        i += 1
        progressBar = ProgressBar()
        progressBar.progress(i, len(engine_urls), status='Searching')
    return sublist


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
        list = []
        sys.stdout.write("- DNS Info\n")
        query_dns(url)
        sys.stdout.write("- Discover subdomains with search engines\n")
        list = query_search(url)
        sys.stdout.write("\n- Brute-forcing subdomains\n")
        sub_brute = SubBrute(url.replace("http://", "http://{fuzz}."), BASE_DIR + "/wordlists/" + "sub.txt")
        list += sub_brute.brute_all()
        # uniquify the list
        uniquelist = uniquify(list)
        sys.stdout.write("- Unique Subdomains: %s\n" % len(uniquelist))
        # print list of subdomains
        sys.stdout.write(''.join(map(str, uniquelist)))
    except KeyboardInterrupt:
        sys.stdout.write(RED)
        sys.stdout.write("Keyboard Interrupt detected. Exiting\n")
        sys.stdout.write(RESET)
        exit(42)


def version():
    sys.stdout.write(banner)


def help():
    sys.stdout.write("subbuster.py -u/--url URL\n")
    sys.stdout.write("Example: subbuster.py -u http://test.net/\n\n")


def main():
    scan()
    sys.exit()


if __name__ == "__main__":
    main()