from django.test import TestCase, Client
from django.utils import unittest
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar

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
    
    # FIXME: test crate capacity
    def test_capacity(self):
        self.assertGreater(self.crate.capacity, self.crate.jars)
    
class JarTestCase(TestCase):
    fixtures = ['inventory', 'catalog']

    def setUp(self):
        self.jar = Jar.objects.all()[0]
        self.client = Client()
            
    def test_unicode(self):
        self.assertEqual(self.jar.__unicode__(), self.jar.name)
    
