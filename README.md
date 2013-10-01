aws_billing
===========

AWS Detailed Billing CSV Parser &amp; Reporting Tool

Setup
-----

See [the AWS docs](http://docs.aws.amazon.com/awsaccountbilling/latest/about/programaccess.html) for how to set up programmatic access to your billing.

Once this is done, a CSV file will be written (and updated) to the bucket you gave on the form.

To use tag-based costs breakdown you need to give a tag like e.g. "BILLING" with a relevant value to your EC2 instances, S3 buckets, ELBs etc.

Otherwise the script will just break down your costs per service and service type (e.g. ec2 * BoxUsage vs ec2 * EBS)

Dependencies
------------

    $ sudo pip install boto cyclone Twisted

Boto should be configured with an access/secret key pair that allows to read from your bucket that holds the detailed billing CSV file. E.g. check your `/etc/boto.cfg` for the `Credentials` section. 


Usage
-----

    $ python -m aws_billing.server <account-id> <bucket-name>

Then point your browser to [localhost:8888](http://localhost:8888/) to see the report. Parsing may be a bit long the first time so be patient. Subsequent calls will be cached for a few minutes though.


Contributing
------------

I'm accepting pull requests !

Many aspects of the program can/should be improved :
* UI (the program is writing raw html, a nice CSS would be great)
* command line options (e.g. argparse)
* parsing (sns topics names should be better recognized)
* tagged vs non-tagged resources costs imputation (one should be able to cross the 2 tables)
* daemon mode
* etc

