# -*- coding:utf-8 -*-
'''
Created on 20 sept. 2013

@author: ediemert
'''

services = {
                'Amazon Simple Storage Service':{'name':'s3'},
                'Amazon Elastic Compute Cloud':{'name':'ec2'},
                'Amazon Route 53':{'name':'r53'},
                'Amazon Simple Notification Service':{'name':'sns'},
                'Amazon Simple Queue Service':{'name':'sqs'},
                'Amazon DynamoDB':{'name':'ddb'},
                'Amazon RDS Service':{'name':'rds'},
                'Amazon Virtual Private Cloud':{'name':'vpc'},
                'Amazon SimpleDB':{'name':'sdb'},
                'Amazon ElastiCache':{'name':'eca'},
                'AWS Data Pipeline':{'name':'adp'},
                'Amazon Elastic MapReduce':{'name':'emr'},
                'Amazon Glacier':{'name':'agl'},
            }

def service_name(product_name):
    return services[product_name]['name']