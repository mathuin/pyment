from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from models import Warehouse, Row, Shelf, Bin, Crate, Jar
from meadery.models import Product
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc


class WarehouseTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)

    def test_unicode(self):
        self.assertEqual(self.warehouse.__unicode__(), self.warehouse.name)

    def test_slug(self):
        self.assertEqual(self.warehouse.slug, 'w1')


class RowTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)

    def test_unicode(self):
        self.assertEqual(self.row.__unicode__(), self.row.name)

    def test_slug(self):
        self.assertEqual(self.row.slug, 'w1-r1')


class ShelfTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)
        self.shelf = Shelf.objects.get(row=self.row, number=1)

    def test_unicode(self):
        self.assertEqual(self.shelf.__unicode__(), self.shelf.name)

    def test_slug(self):
        self.assertEqual(self.shelf.slug, 'w1-r1-s1')


class BinTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)
        self.shelf = Shelf.objects.get(row=self.row, number=1)
        self.bin = Bin.objects.get(shelf=self.shelf, number=1)

    def test_unicode(self):
        self.assertEqual(self.bin.__unicode__(), self.bin.name)

    def test_slug(self):
        self.assertEqual(self.bin.slug, 'w1-r1-s1-b1')

    def test_capacity(self):
        # one crate in a two-crate bin
        self.assertGreater(self.bin.capacity, self.bin.crates)
        new_crate = Crate(number=37, bin=self.bin)
        new_crate.save()
        # just saved a second crate, still okay!
        self.assertEqual(self.bin.capacity, self.bin.crates)
        newer_crate = Crate(number=38, bin=self.bin)
        # saving this third crate should cause clean to throw a ValidateError
        # NB: calling .save() bypasses .clean()
        self.assertRaises(ValidationError, newer_crate.clean())


class CrateTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.crate = Crate.objects.all()[0]

    def test_unicode(self):
        self.assertEqual(self.crate.__unicode__(), self.crate.name)

    def test_capacity(self):
        self.assertGreater(self.crate.capacity, self.crate.jars)

    def test_slug(self):
        self.assertEqual(self.crate.slug, 'c1')


class JarTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.jar = Jar.objects.all()[0]

    def test_unicode(self):
        self.assertEqual(self.jar.__unicode__(), self.jar.name)

    def test_delete_old_jars(self):
        all_count = Jar.objects.count()
        remove_before = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        deletable_count = Jar.objects.filter(is_active=False, updated_at__lt=remove_before).count()
        remaining_count = all_count - deletable_count
        # Try with dry run enabled.
        # No error should be raised, no jars should be deleted.
        args = []
        opts = {'dryrun': True}
        call_command('delete_old_jars', *args, **opts)
        self.assertEqual(Jar.objects.all().count(), all_count)
        # Try without dry run enabled.
        # No error should be raised, all jars should be deleted.
        args = []
        opts = {}
        call_command('delete_old_jars', *args, **opts)
        self.assertEqual(Jar.objects.all().count(), remaining_count)

    def test_add_new_jars(self):
        # Products: good is known to exist, bad is known *not* to exist.
        good_product = Product.objects.get(slug='sip-1-a')
        good_product_name = good_product.name
        bad_product = Product.objects.get(slug='sip-1-b')
        bad_product_name = bad_product.name
        bad_product.delete()
        # Crates: good is known to exist, saving bad for last.
        good_crate = Crate.objects.get(slug='c2')
        good_crate_number = good_crate.number
        # Fill up the good crate!
        num_jars = good_crate.capacity - good_crate.jars
        # Choose the next jar in the good product.
        start_jar = max(Jar.objects.filter(product=good_product).values_list('number', flat=True)) + 1
        end_jar = start_jar + num_jars - 1
        good_crate_jars = good_crate.jars
        # Try adding non-existent product to good crate.
        # CommandError should be raised, no new jars should be added.
        args = []
        opts = {'product': bad_product_name,
                'start_jar': start_jar,
                'end_jar': end_jar,
                'crate': good_crate_number}
        try:
            call_command('add_new_jars', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Not a valid product: %s' % bad_product_name)
        else:
            self.fail('Adding bad product to good crate should have failed.')
        self.assertEqual(good_crate.jars, good_crate_jars)
        # Try a start jar that's greater than an end jar.
        # CommandError should be raised, no new jars should be added.
        args = []
        opts = {'product': good_product_name,
                'start_jar': end_jar,
                'end_jar': start_jar,
                'crate': good_crate_number}
        try:
            call_command('add_new_jars', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Start jar value must be less than or equal to end jar value')
        else:
            self.fail('Start jar greater than end jar should have failed.')
        self.assertEqual(good_crate.jars, good_crate_jars)
        # Try with dry run enabled.
        # No error should be raised, no new jars should be added.
        args = []
        opts = {'product': good_product_name,
                'start_jar': start_jar,
                'end_jar': end_jar,
                'crate': good_crate_number,
                'dryrun': True}
        call_command('add_new_jars', *args, **opts)
        self.assertEqual(good_crate.jars, good_crate_jars)
        # Try without dry run enabled.
        # No error should be raised, but new jars should be added.
        args = []
        opts = {'product': good_product_name,
                'start_jar': start_jar,
                'end_jar': end_jar,
                'crate': good_crate_number}
        call_command('add_new_jars', *args, **opts)
        self.assertEqual(good_crate.jars, good_crate_jars + num_jars)
        # Try adding one more jar to that full crate.
        # CommandError should be raised, no new jars should be added.
        good_crate_jars = good_crate.jars
        num_jars = 1
        start_jar = end_jar + 1
        end_jar = start_jar + num_jars - 1
        args = []
        opts = {'product': good_product_name,
                'start_jar': start_jar,
                'end_jar': end_jar,
                'crate': good_crate_number}
        try:
            call_command('add_new_jars', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Crate capacity would be exceeded: %d > %d' % (good_crate.capacity + num_jars, good_crate.capacity))
        else:
            self.fail('Exceeding crate capacity should have failed.')
        self.assertEqual(good_crate.jars, good_crate_jars)
        # Delete the crate and try to add jars to it.
        # CommandError should be raised, no new jars should be added.
        good_crate.delete()
        opts = {'product': good_product_name,
                'start_jar': start_jar,
                'end_jar': end_jar,
                'crate': good_crate_number}
        try:
            call_command('add_new_jars', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Not a valid crate: %d' % good_crate_number)
        else:
            self.fail('Invalid crate should have failed.')

    def test_crate_transfer(self):
        full_crate = Crate.objects.get(slug='c3')
        full_crate_jars = full_crate.jars
        empty_crate = Crate.objects.get(slug='c2')
        empty_crate_jars = empty_crate.jars
        partial_crate = Crate.objects.get(slug='c1')
        partial_crate_jars = partial_crate.jars
        # Try using full crate as destination.
        # CommandError should be raised, no jars should move.
        args = []
        opts = {'source': partial_crate.number,
                'dest': full_crate.number}
        try:
            call_command('crate_transfer', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Destination crate does not have enough room')
        else:
            self.fail('A full destination crate should have failed.')
        self.assertEqual(partial_crate.jars, partial_crate_jars)
        self.assertEqual(full_crate.jars, full_crate_jars)
        # Try using empty crate as source.
        # CommandError should be raised, no jars should move.
        args = []
        opts = {'source': empty_crate.number,
                'dest': full_crate.number}
        try:
            call_command('crate_transfer', *args, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Source crate is empty')
        else:
            self.fail('An empty source crate should have failed.')
        self.assertEqual(empty_crate.jars, empty_crate_jars)
        self.assertEqual(full_crate.jars, full_crate_jars)
        # Try with dry run enabled.
        # No error should be raised, but no jars should move.
        args = []
        opts = {'source': partial_crate.number,
                'dest': empty_crate.number,
                'dryrun': True}
        call_command('crate_transfer', *args, **opts)
        self.assertEqual(partial_crate.jars, partial_crate_jars)
        self.assertEqual(empty_crate.jars, empty_crate_jars)
        # Try without dry run enabled.
        # No error should be raised, and jars should move.
        args = []
        opts = {'source': partial_crate.number,
                'dest': empty_crate.number}
        call_command('crate_transfer', *args, **opts)
        self.assertEqual(partial_crate.jars, empty_crate_jars)
        self.assertEqual(empty_crate.jars, partial_crate_jars)

    def test_crate_utilization(self):
        # JMT: write this
        # This test needs:
        #  - one new product
        #  - one new crate with 12 jars of said new product
        # JMT: actually, I may defer writing these tests.
        # I am thinking of making this a view instead of a command.
        # An option on the warehouse-level inventory views.
        pass
