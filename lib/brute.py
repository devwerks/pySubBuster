import sys
import urllib2
from utils.colors import *


class SubBrute:

    def __init__(self, url, wordlist):

        self.target = url
        self.wordlist = wordlist
        self.useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"
        self.timeout = 200
        self.pError = False

    def printRed(self, string, error):
        errorstring = RED + "%s" % string + " (error: %s)\n" % error + RESET
        sys.stdout.write(errorstring)

    def createurl(self, url, word):
        if url.find("{fuzz}") != -1:
            return url.replace("{fuzz}", word)
        else:
            newurl = url + word
            return newurl

    def request(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header("User-agent", self.useragent)
            response = urllib2.urlopen(req, timeout=self.timeout)
            data = response.read()
            output = GREEN + "%s (size: %s)\n" % (url, len(data)) + RESET
            sys.stdout.write(output)
        except urllib2.HTTPError, e:
            if self.pError:
                self.printRed(url, e.code)
        except urllib2.URLError, e:
            if self.pError:
                self.printRed(url, e.args)

    def brute_all(self):
        with open(self.wordlist) as f:
            for line in f:
                newurl = self.createurl(self.target.rstrip(), line.rstrip())
                self.request(newurl)
