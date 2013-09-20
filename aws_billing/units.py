# -*- coding:utf-8 -*-
'''
Created on 20 sept. 2013

@author: ediemert
'''

unit_transforms = { 
    'ByteHrs':{'transform':lambda x: x,
               'unit':'GB'},
    'Requests':{'transform':lambda x:x,
                'unit':'requests'},
    'BoxUsage':{'transform':lambda x:int(x),
                'unit':'hours'},
    'VolumeUsage':{'transform':lambda x:int(x),
                   'unit':'GB'},
    'VolumeP-IOPS.piops':{'transform':lambda x:int(x),
                          'unit':'GB'},
    'LoadBalancerUsage':{'transform':lambda x:int(x),
                          'unit':'hours'},
    'DataTransfer':{'transform':lambda x:x/(1024**3),
                    'unit':'GB'},
    'DNS-Queries':{'transform':lambda x:x/(1024**3),
                    'unit':'requests'},
    'ReadCapacityUnit-Hrs':{'transform':lambda x:int(x),
                          'unit':'hours'},
                   }

def unitize(usage_type, usage_quantity):
    for unit, unit_data in unit_transforms.iteritems():
        if unit in usage_type:
            s = "%.2f %s"%(unit_data['transform'](usage_quantity),
                           unit_data['unit'])
            return s
    #print "XOXOX","unknown usage type: <%s>"%usage_type
    return "%f (unknown unit)"%usage_quantity
