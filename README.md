aws_billing
===========

AWS Detailed Billing CSV Parser &amp; Reporting Tool

Setup
-----

See [the AWS docs](http://docs.aws.amazon.com/awsaccountbilling/latest/about/programaccess.html) for how to set up programmatic access to your billing.

Once this is done, a CSV file will be written (and updated) to the bucket you gave on the form.

To use tag-based costs breakdown you need to give a tag like e.g. "BILLING" with a relevant value to your EC2 instances, S3 buckets, ELBs etc.

Otherwise the script will just break down your costs per service and service type (e.g. ec2 * BoxUsage vs ec2 * EBS)

Usage
-----

Command-line mode
~~~~~~~~~~~~~~~~~

    $ python -m aws_billing.driver <account-id> <bucket-name>


Server mode
~~~~~~~~~~~~~~~~~

    $ python -m aws_billing.server <account-id> <bucket-name>


Then point your browser to `localhost:8888/` to see the report. Parsing is a bit long so be patient.

Contributing
------------

I'm accepting pull requests. Many aspects of the program can/should be improved !


