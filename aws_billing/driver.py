# -*- coding:utf-8 -*-
'''
Created on 9 sept. 2013

@author: ediemert
'''

from datetime import datetime
import zipfile
import os.path, time
from aws_billing.parser import parse
from boto import connect_s3

def is_recent_enough(fn, delta_secs=60*10):
    if os.path.exists(fn):
        created_at = os.path.getctime(fn)
        time_delta = time.time() - created_at
        if time_delta < delta_secs:
            return True
    return False

def retrieve_fd(account="920279639305", bucket_name="bom-billing", month=None,
                tmp_dir='.'):
    month = month or datetime.now().strftime('%Y-%m')
    fn = "%s-aws-billing-detailed-line-items-with-resources-and-tags-%s.csv"%(account, month)
    if not is_recent_enough(fn):
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
