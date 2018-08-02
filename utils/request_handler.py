import sys
import urllib2
from utils.colors import *


class RequestHandler:

    def __init__(self, head=False, timeout=200):
        self.head = head
        self.timeout = timeout
        self.pError = False

    def printRed(self, string, error):
        errorstring = RED + "%s" % string + " (error: %s)\n" % error + RESET
        sys.stdout.write(errorstring)

    def send(self, url):
        try:
            req = urllib2.Request(url)
            if self.head:
                req.get_method = lambda: "HEAD"
            req.add_header("User-agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0")
            response = urllib2.urlopen(req, timeout=self.timeout)
            return response.read()
        except urllib2.HTTPError, e:
            if self.pError:
                self.printRed(url, e.code)
        except urllib2.URLError, e:
            if self.pError:
                self.printRed(url, e.args)
