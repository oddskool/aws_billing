# -*- coding:utf-8 -*-
'''
Created on 20 sept. 2013

@author: ediemert
'''

import csv
from collections import defaultdict
from aws_billing.services import service_name

def add_type(d):
    if d['RecordType'] != 'LineItem':
        return None
    for field in ('Cost', 'UsageQuantity'):
        d[field] = float(d[field] if len(d[field]) else 1)
    for field in ('LinkedAccountId', 'InvoiceID', 'RecordType', 'RecordId',
                  'PayerAccountId', 'SubscriptionId'):
        del d[field]
    return d

def forge_key(d):
    service = service_name(d['ProductName'])
    resource_tag = d.get('user:BILLING', None)
    yield 'Total * Total'
    if resource_tag:
        yield ' * '.join(("BILLING", resource_tag))
    else:
        if d["ItemDescription"] == 'Tax of type VAT':
            yield "tva"
        else:
            yield ' * '.join(("BILLING", 'untagged'))
    #if not resource_tag:
    if service == 'ec2':
        resource_tag = d['UsageType'].split(':')[0]
        if '-' in resource_tag:
            resource_tag = resource_tag.split('-')[1]
    else:
        resource_tag = d['ResourceId']
    if not d["ItemDescription"] == 'Tax of type VAT':
        yield ' * '.join((service,
                          resource_tag))

def parse_line(stats, d):
    d = add_type(d)
    if not d:
        return
    for key in forge_key(d):
        stats[key]['Cost'] += d['Cost']
        stats[key]['UsageQuantity'] += d['UsageQuantity']

def parse(fd, price_floor_dollars=0.1):
    reader = csv.reader(fd, delimiter=',', quotechar='"')
    legend = None
    stats = defaultdict(lambda: defaultdict(int))
    for i, row in enumerate(reader):
        if not legend:
            legend = row
            continue
        d = dict(zip(legend, row))
        try:
            parse_line(stats, d)
        except Exception as e:
            print "Exception:", type(e), e
            print d
        if i and not i % 10000:
            print i,"lines..."
    stats = [ (resource, cost_usage) for resource, cost_usage in 
                stats.iteritems() if cost_usage['Cost'] > price_floor_dollars ]
    stats.sort(key=lambda x:x[-1]['Cost'], reverse=True)
    return stats

