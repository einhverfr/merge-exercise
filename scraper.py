"""
This is a simple scraping utility that reads a list or urls from
a file and checks to see if we get a valid response.
"""

import csv
from urllib import request
import http
import urllib
from bs4 import BeautifulSoup

def status_of(hostname):
    """
    This functon accepts a url as hostname and returns a status
    dictionary
    """
    urlstatus = {}
    try:
        urlstatus["page"] = request.urlopen(hostname).read()
        bsparse = BeautifulSoup(urlstatus["page"], 'html.parser')
        urlstatus["status"] = bool(bsparse.body)
        urlstatus["exception"] = ''
    except (http.client.RemoteDisconnected, urllib.error.URLError) as e:
        urlstatus["status"] = False
        urlstatus["exception"] = e
    return urlstatus


def processfile(filename):
    """
    Takes a filename in, andreturns a dictionary of status
    dictionaries
    """
    with open('hosts') as f:
        csvr = csv.reader(f)
        urls = {x[0]: status_of(x[0]) for x in csvr }
    return urls

def printreport(urls):
    """
    Takes in a dictionary of status dictionaries and returns
    a report
    """
    reportline = "{:<30}|{:7}|{:40}"
    reportstrings = [];
#    def print(string):
#        reportstrings.append(string)
    reportstrings.append(reportline.format('URL', 'Up', 'Exception'))
    reportstrings.append(reportline.format('=' * 30, '=' * 7, '=' * 40))
    for url in urls:
       reportstrings.append(reportline.format(url, urls[url]["status"], str(urls[url]["exception"])))
    return "\n".join(reportstrings)



if __name__ == '__main__':
    print(printreport(processfile("hosts")))
