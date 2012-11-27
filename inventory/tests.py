from django.test import TestCase, Client
from django.core.management import call_command
from django.core.management.base import CommandError
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from catalog.models import Product
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc
from inventory.management.commands import add_new_jars

class WarehouseTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.warehouse = Warehouse.objects.all()[0]
        self.client = Client()
    
    def test_unicode(self):
        self.assertEqual(self.warehouse.__unicode__(), self.warehouse.name)
    
class RowTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.row = Row.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.row.__unicode__(), self.row.name)
    
class ShelfTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.shelf = Shelf.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.shelf.__unicode__(), self.shelf.name)
    
class BinTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.bin = Bin.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.bin.__unicode__(), self.bin.name)
    
    # FIXME: test bin capacity
    
class CrateTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.crate = Crate.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.crate.__unicode__(), self.crate.name)
    
    def test_capacity(self):
        self.assertGreater(self.crate.capacity, self.crate.jars)
    
class JarTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.jar = Jar.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.jar.__unicode__(), self.jar.name)
    
    def test_delete_old_jars(self):
        all_count = Jar.objects.count()
        remove_before = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        deletable_count = Jar.objects.filter(is_active=False,updated_at__lt=remove_before).count()
        remaining_count = all_count - deletable_count
        call_command('delete_old_jars')
        self.assertEqual(Jar.objects.all().count(), remaining_count)
        
    def test_add_new_jars(self):
        good_product = Product.objects.all()[0]
        good_product_name = good_product.name
        bad_product_name = good_product.name + 'A'
        good_crate = Crate.objects.all()[0]
        good_crate_name = good_crate.name
        bad_crate_name = good_crate.name + '1'
        num_jars = 2
        start_jar = 4
        end_jar = start_jar + num_jars - 1
        good_crate_jars = good_crate.jars
        # try to add two jars of existing product to imaginary crate
        # CommandError expected
        self.assertRaises(SystemExit, call_command, 'add_new_jars', good_product_name, start_jar, end_jar, bad_crate_name)
        # try to add two jars of imaginary product to existing crate
        # CommandError expected
        self.assertRaises(SystemExit, call_command, 'add_new_jars', bad_product_name, start_jar, end_jar, good_crate_name)
        call_command('add_new_jars', good_product_name, start_jar, end_jar, good_crate_name)
        # number of jars in existing crate should go up by two
        self.assertEqual(good_crate.jars, good_crate_jars + num_jars)
        # optional - confirm that new jars are the correct jars