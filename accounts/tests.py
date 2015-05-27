from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# profile.py
# testing order_info below covers this

# views.py
# test register -- this gets us .. nothing else
# - both paths (get and post)
# test my_account (just get)
# test order_details
# test order_info (get and post)
