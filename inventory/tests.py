from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from models import Warehouse, Row, Shelf, Bin, Crate, Jar
from meadery.models import Product
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.utils.six import StringIO


# admin.py
# link_rows in warehouse -- check admin page?
# link_shelves link_bins  .. I sense a trend

# add_new_jars.py
# more edge cases on exceptions?
# same for crate transfer

# crate utilization isn't even tested!


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
        self.out = StringIO()

    def test_unicode(self):
        self.assertEqual(self.jar.__unicode__(), self.jar.name)

    def test_crate_transfer(self):
        full_crate = Crate.objects.get(slug='c3')
        full_crate_jars = full_crate.jars
        empty_crate = Crate.objects.get(slug='c2')
        empty_crate_jars = empty_crate.jars
        partial_crate = Crate.objects.get(slug='c1')
        partial_crate_jars = partial_crate.jars
        # Try using full crate as destination.
        # CommandError should be raised, no jars should move.
        opts = {'source': partial_crate.number,
                'dest': full_crate.number}
        try:
            call_command('crate_transfer', stdout=self.out, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Destination crate does not have enough room')
        else:
            self.fail('A full destination crate should have failed.')
        self.assertEqual(partial_crate.jars, partial_crate_jars)
        self.assertEqual(full_crate.jars, full_crate_jars)
        # Try using empty crate as source.
        # CommandError should be raised, no jars should move.
        opts = {'source': empty_crate.number,
                'dest': full_crate.number}
        try:
            call_command('crate_transfer', stdout=self.out, **opts)
        except CommandError as e:
            self.assertEqual(e.args[0], 'Source crate is empty')
        else:
            self.fail('An empty source crate should have failed.')
        self.assertEqual(empty_crate.jars, empty_crate_jars)
        self.assertEqual(full_crate.jars, full_crate_jars)
        # Try with dry run enabled.
        # No error should be raised, but no jars should move.
        opts = {'source': partial_crate.number,
                'dest': empty_crate.number,
                'dryrun': True}
        call_command('crate_transfer', stdout=self.out, **opts)
        self.assertEqual(partial_crate.jars, partial_crate_jars)
        self.assertEqual(empty_crate.jars, empty_crate_jars)
        # Try without dry run enabled.
        # No error should be raised, and jars should move.
        opts = {'source': partial_crate.number,
                'dest': empty_crate.number}
        call_command('crate_transfer', stdout=self.out, **opts)
        self.assertEqual(partial_crate.jars, empty_crate_jars)
        self.assertEqual(empty_crate.jars, partial_crate_jars)


class AddNewJarsTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.out = StringIO()

        # Products: good is known to exist, bad is known *not* to exist.
        good_product = Product.objects.get(slug='sip-1-a')
        self.good_product_name = good_product.name
        bad_product = Product.objects.get(slug='sip-1-b')
        self.bad_product_name = bad_product.name
        bad_product.delete()

        # Crates: good is known to exist, saving bad for last.
        self.good_crate = Crate.objects.get(slug='c2')
        self.good_crate_number = self.good_crate.number

        # Fill up the good crate!
        self.num_jars = self.good_crate.capacity - self.good_crate.jars
        # Choose the next jar in the good product.
        self.good_start_jar = max(Jar.objects.filter(product=good_product).values_list('number', flat=True)) + 1
        self.good_end_jar = self.good_start_jar + self.num_jars - 1
        self.good_crate_jars = self.good_crate.jars

    # add_new_jars_commanderror
    def anj_ce(func):
        def _decorator(self, *args, **kwds):
            func(self, *args, **kwds)
            opts = {'product': self.product,
                    'start_jar': self.start_jar,
                    'end_jar': self.end_jar,
                    'crate': self.crate_number}
            try:
                call_command('add_new_jars', stdout=self.out, **opts)
            except CommandError as e:
                self.assertEqual(e.args[0], self.error)
            else:
                self.fail("Should have failed with {0}".format(self.error))
            self.assertEqual(self.good_crate.jars, self.good_crate_jars)
        return _decorator

    @anj_ce
    def test_anj_ce_product_required(self):
        self.product = ''
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = 'Product required!'

    @anj_ce
    def test_anj_ce_not_valid_product(self):
        # Try adding non-existent product to good crate.
        self.product = self.bad_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = 'Not a valid product: {0}'.format(self.product)

    @anj_ce
    def test_anj_ce_start_not_less_than_end(self):
        # Try a start jar that's greater than an end jar.
        self.product = self.good_product_name
        self.start_jar = self.good_end_jar
        self.end_jar = self.good_start_jar
        self.crate_number = self.good_crate_number
        self.error = 'Start jar value must be less than or equal to end jar value'

    @anj_ce
    def test_anj_ce_exceed_capacity(self):
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar + 1
        self.crate_number = self.good_crate_number
        self.error = 'Crate capacity would be exceeded: {0} > {1}'.format(self.good_crate.capacity + 1, self.good_crate.capacity)

    @anj_ce
    def test_anj_ce_bad_crate(self):
        # Delete the crate and try to add jars to it.
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar + 1
        self.crate_number = self.good_crate_number + 10
        self.error = 'Not a valid crate: {0}'.format(self.crate_number)

    def test_add_new_jars(self):
        # Try with dry run enabled.
        # No error should be raised, no new jars should be added.
        opts = {'product': self.good_product_name,
                'start_jar': self.good_start_jar,
                'end_jar': self.good_end_jar,
                'crate': self.good_crate_number,
                'dryrun': True}
        call_command('add_new_jars', stdout=self.out, **opts)
        self.assertEqual(self.good_crate.jars, self.good_crate_jars)
        # Try without dry run enabled.
        # No error should be raised, but new jars should be added.
        opts = {'product': self.good_product_name,
                'start_jar': self.good_start_jar,
                'end_jar': self.good_end_jar,
                'crate': self.good_crate_number}
        call_command('add_new_jars', stdout=self.out, **opts)
        self.assertEqual(self.good_crate.jars, self.good_crate_jars + self.num_jars)


class DeleteOldJarsTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.out = StringIO()

    def test_delete_old_jars(self):
        all_count = Jar.objects.count()
        remove_before = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        deletable_count = Jar.objects.filter(is_active=False, updated_at__lt=remove_before).count()
        remaining_count = all_count - deletable_count
        # Try with dry run enabled.
        # No error should be raised, no jars should be deleted.
        opts = {'dryrun': True}
        call_command('delete_old_jars', stdout=self.out, **opts)
        self.assertEqual(Jar.objects.all().count(), all_count)
        # Try without dry run enabled.
        # No error should be raised, all jars should be deleted.
        call_command('delete_old_jars', stdout=self.out)
        self.assertEqual(Jar.objects.all().count(), remaining_count)


class CrateUtilizationTestCase(TestCase):
    fixtures = ['inventory', 'meadery']

    def setUp(self):
        self.out = StringIO()
        self.good_warehouse_number = Warehouse.objects.get(number=1).number

    # crate_utilization_commanderror
    def cu_ce(func):
        def _decorator(self, *args, **kwds):
            func(self, *args, **kwds)
            opts = {}
            try:
                opts['warehouse'] = self.warehouse_number
            except AttributeError:
                pass
            try:
                call_command('crate_utilization', stdout=self.out, **opts)
            except CommandError as e:
                self.assertEqual(e.args[0], self.error)
            else:
                self.fail("Should have failed with {0}".format(self.error))
        return _decorator

    @cu_ce
    def test_cu_ce_not_int(self):
        self.warehouse_number = 'x'
        self.error = 'Warehouse not an int: {0}'.format(self.warehouse_number)

    @cu_ce
    def test_cu_ce_does_not_exist(self):
        self.warehouse_number = self.good_warehouse_number + 10
        self.error = 'Not a valid warehouse number: {0}'.format(self.warehouse_number)

    def test_crate_utilization(self):
        opts = {'warehouse': self.good_warehouse_number}
        try:
            call_command('crate_utilization', stdout=self.out, **opts)
        except CommandError as e:
            self.fail("Failed with {0}".format(e.args[0]))
        # JMT: this "expected output" is very lame.
        # it would be Smart to have the following:
        # one full crate
        # one empty crate
        # one half-full crate
        # I could then test full and empty as well as normal
        expected = 'Crate ID |         Bin         | Capacity | Jars \n==================================================\n'
        self.assertEqual(expected, self.out.getvalue())
