# -*- coding:utf-8 -*-
'''
Created on 20 sept. 2013

@author: ediemert
'''

import sys
import time

import cyclone.web
from twisted.internet import reactor
from twisted.python import log

from aws_billing.driver import retrieve_fd
from aws_billing.parser import parse


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        try:
            self._get()
        except Exception as e:
            print e
            raise e
    def _get(self):
        self.write("<h1>Aws Billing Parser</h1>")
        self.write("<p>retrieving data... ")
        self.flush()
        now = time.time()
        if not self.application.read_time or (now - self.application.read_time) > 60*10:
            fd = retrieve_fd(self.application.account_id,
                             self.application.bucket_name)
            self.write("parsing data...</p>")
            self.flush()
            self.application.stats = parse(fd)
            self.application.read_time = now
        self.write("<h2>Tag Based Billing Report</h2><table><tr><th>Billing Tag</th><th>Cost ($)</th></tr>")
        for d in self.application.stats:
            if 'BILLING' in d[0]:
                self.write("<tr><td>%s</td><td>%.2f</td></tr>" % (d[0][10:],d[1]['Cost']))
        self.write("</table>")
        self.write("<h2>Resource Type Based Billing Report</h2><table><tr><th>Billing Tag</th><th>Cost ($)</th></tr>")
        for d in self.application.stats:
            if 'BILLING' not in d[0]:
                self.write("<tr><td>%s</td><td>%.2f</td></tr>" % (d[0],d[1]['Cost']))
        self.write("</table>")
        self.write("</p><tiny><a href='https://github.com/oddskool/aws_billing'>Fork me on Github !</a></tiny></p>")

if __name__ == "__main__":
    application = cyclone.web.Application([(r"/", MainHandler)])
    application.account_id = sys.argv[1]
    application.bucket_name = sys.argv[2]
    application.stats = None
    application.read_time = None
    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application, interface="")
    reactor.run()