import sys
import urllib2
from utils.colors import *


class RequestHandler:

    def __init__(self, timeout=200):
        self.timeout = timeout

    def send(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header("User-agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0")
            response = urllib2.urlopen(req, timeout=self.timeout)
            return response.read()
        except:
            sys.stdout.write(RED)
            sys.stdout.write("Error connecting to host\n")
            sys.stdout.write(RESET)
