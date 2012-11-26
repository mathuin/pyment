from django.test import TestCase, Client
from django.core.management import call_command
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc

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