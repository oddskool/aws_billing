# -*- coding:utf-8 -*-
'''
Created on 20 sept. 2013

@author: ediemert
'''

import cyclone.web
import sys

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
        self.write("<p>retrieving data...</p>")
        self.flush()
        fd = retrieve_fd()
        self.write("<p>parsing data...</p>")
        self.flush()
        stats = parse(fd)
        self.write("<h2>Tag Based Billing Report</h2><table><tr><th>Billing Tag</th><th>Cost ($)</th></tr>")
        for d in stats:
            if 'BILLING' in d[0]:
                self.write("<tr><td>%s</td><td>%.2f</td></tr>"%(d[0][10:],d[1]['Cost']))
        self.write("</table>")
        self.write("<h2>Resource Type Based Billing Report</h2><table><tr><th>Billing Tag</th><th>Cost ($)</th></tr>")
        for d in stats:
            if 'BILLING' not in d[0]:
                self.write("<tr><td>%s</td><td>%.2f</td></tr>"%(d[0][10:],d[1]['Cost']))
        self.write("</table>")
        self.write("</p><tiny><a href='https://github.com/oddskool/aws_billing'>Fork me on Github !</a></tiny></p>")

application = cyclone.web.Application([(r"/", MainHandler)])

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application, interface="")
    reactor.run()