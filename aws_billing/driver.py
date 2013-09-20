# -*- coding:utf-8 -*-
'''
Created on 9 sept. 2013

@author: ediemert
'''

from datetime import datetime
import zipfile
import os.path
from boto import connect_s3
from aws_billing.parser import parse

def retrieve_fd(account, bucket_name, month=None, tmp_dir='.'):
    month = month or datetime.now().strftime('%Y-%m')
    fn = "%s-aws-billing-detailed-line-items-with-resources-and-tags-%s.csv"%(account, month)
    s3 = connect_s3()
    bucket = s3.get_bucket(bucket_name)
    key = bucket.get_key(fn+'.zip')
    key.get_contents_to_filename(os.path.join(tmp_dir, fn+'.zip'))
    return zipfile.ZipFile(os.path.join(tmp_dir,fn+'.zip')).open(fn)

if __name__ == '__main__':
    fd = retrieve_fd()
    stats = parse(fd)
    for d in stats:
        print "%s : $%.2f " % (d[0],
                               d[1]['Cost'])#,
                                   #unitize(d[0], d[1]['UsageQuantity']))
