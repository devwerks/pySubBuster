import sys
import threading
from utils.colors import *
from utils.request_handler import RequestHandler
from utils.progress_bar import ProgressBar

class SubBrute:

    def __init__(self, url, wordlist):

        self.target = url
        self.wordlist = wordlist
        self.useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"
        self.timeout = 60
        self.pError = False
        self.sublist = []

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
        request_handler = RequestHandler()
        data = request_handler.send(url)
        if data:
            output = GREEN + "%s\n" % url.replace("http://", "") + RESET
            self.sublist.append(output)

    def brute_all(self):
        threads = []
        num_lines = sum(1 for line in open(self.wordlist))
        count = 0
        with open(self.wordlist) as f:
            for line in f:
                newurl = self.createurl(self.target.rstrip(), line.rstrip())
                at = threading.activeCount()
                if at <= 10:
                    thread = threading.Thread(target=self.request, args=(newurl,))
                    threads.append(thread)
                    thread.start()
                else:
                    self.request(newurl)
                count += 1
                progressBar = ProgressBar()
                progressBar.progress(count, num_lines, status='Brute-forcing')
            sys.stdout.write('\n- Wait for all threads to finish\n')
            for x in threads:
                x.join()
            return self.sublist
