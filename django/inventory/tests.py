from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from meadery.models import Product
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc
from io import StringIO


# admin.py
# link_rows in warehouse -- check admin page?
# link_shelves link_bins  .. I sense a trend


class WarehouseTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)

    def test_str(self):
        self.assertEqual(self.warehouse.__str__(), self.warehouse.name)

    def test_slug(self):
        self.assertEqual(self.warehouse.slug, "w1")


class RowTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)

    def test_str(self):
        self.assertEqual(self.row.__str__(), self.row.name)

    def test_slug(self):
        self.assertEqual(self.row.slug, "w1-r1")


class ShelfTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)
        self.shelf = Shelf.objects.get(row=self.row, number=1)

    def test_str(self):
        self.assertEqual(self.shelf.__str__(), self.shelf.name)

    def test_slug(self):
        self.assertEqual(self.shelf.slug, "w1-r1-s1")


class BinTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.warehouse = Warehouse.objects.get(number=1)
        self.row = Row.objects.get(warehouse=self.warehouse, number=1)
        self.shelf = Shelf.objects.get(row=self.row, number=1)
        self.bin = Bin.objects.get(shelf=self.shelf, number=1)

    def test_str(self):
        self.assertEqual(self.bin.__str__(), self.bin.name)

    def test_slug(self):
        self.assertEqual(self.bin.slug, "w1-r1-s1-b1")

    def test_capacity(self):
        # one crate in a two-crate bin
        self.assertGreater(self.bin.capacity, self.bin.crates)
        new_crate = Crate(number=37, bin=self.bin)
        new_crate.save()
        # just saved a second crate, still okay!
        self.assertEqual(self.bin.capacity, self.bin.crates)
        newer_crate = Crate(number=38, bin=self.bin)
        # not saving this third crate should cause clean to throw a TypeError
        # NB: calling .save() bypasses .clean()
        with self.assertRaises(TypeError):
            newer_crate.clean()


class CrateTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.crate = Crate.objects.all()[0]

    def test_str(self):
        self.assertEqual(self.crate.__str__(), self.crate.name)

    def test_capacity(self):
        self.assertGreater(self.crate.capacity, self.crate.jars)

    def test_slug(self):
        self.assertEqual(self.crate.slug, "c1")


class JarTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.jar = Jar.objects.all()[0]
        self.out = StringIO()

    def test_str(self):
        self.assertEqual(self.jar.__str__(), self.jar.name)


class CrateTransferTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.out = StringIO()

        # Full crate
        self.full_crate = Crate.objects.get(slug="c3")
        self.empty_crate = Crate.objects.get(slug="c2")
        self.partial_crate = Crate.objects.get(slug="c1")

    def ct_ce(func):
        def _decorator(self, *args, **kwds):
            source_jars = self.source.jars
            dest_jars = self.dest.jars
            opts = {"source": self.source.number, "dest": self.dest.number}
            try:
                call_command("crate_transfer", stdout=self.out, **opts)
            except CommandError as e:
                self.assertEqual(e.args[0], self.error)
            else:
                self.fail("Should have failed with {}".format(self.error))
            self.assertEqual(self.source.jars, source_jars)
            self.assertEqual(self.dest.jars, dest_jars)

        return _decorator

    @ct_ce
    def ct_ce_no_room(self):
        # Try using full crate as destination.
        self.source = self.partial_crate
        self.dest = self.full_crate
        self.error = "Destination crate does not have enough room"

    @ct_ce
    def ct_ce_no_jars(self):
        # Try using full crate as destination.
        self.source = self.empty_crate
        self.dest = self.full_crate
        self.error = "Source crate is empty"

    def test_crate_transfer_dryrun(self):
        # Try with dry run enabled.
        # No error should be raised, but no jars should move.
        partial_crate_jars = self.partial_crate.jars
        empty_crate_jars = self.empty_crate.jars
        opts = {"source": self.partial_crate.number, "dest": self.empty_crate.number, "dryrun": True}
        call_command("crate_transfer", stdout=self.out, **opts)
        self.assertEqual(self.partial_crate.jars, partial_crate_jars)
        self.assertEqual(self.empty_crate.jars, empty_crate_jars)

    def test_crate_transfer_good(self):
        # Try without dry run enabled.
        # No error should be raised, and jars should move.
        partial_crate_jars = self.partial_crate.jars
        empty_crate_jars = self.empty_crate.jars
        opts = {"source": self.partial_crate.number, "dest": self.empty_crate.number}
        call_command("crate_transfer", stdout=self.out, **opts)
        self.assertEqual(self.partial_crate.jars, empty_crate_jars)
        self.assertEqual(self.empty_crate.jars, partial_crate_jars)


class AddNewJarsTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.out = StringIO()

        # Products: good is known to exist, bad is known *not* to exist.
        good_product = Product.objects.get(slug="sip-1-a")
        self.good_product_name = good_product.name
        bad_product = Product.objects.get(slug="sip-1-b")
        self.bad_product_name = bad_product.name
        bad_product.delete()

        # Crates: good is known to exist, saving bad for last.
        self.good_crate = Crate.objects.get(slug="c2")
        self.good_crate_number = self.good_crate.number

        # Fill up the good crate!
        self.num_jars = self.good_crate.capacity - self.good_crate.jars
        # Choose the next jar in the good product.
        self.good_start_jar = max(Jar.objects.filter(product=good_product).values_list("number", flat=True)) + 1
        self.good_end_jar = self.good_start_jar + self.num_jars - 1
        self.good_crate_jars = self.good_crate.jars

    # add_new_jars_commanderror
    def anj_ce(func):
        def _decorator(self, *args, **kwds):
            func(self, *args, **kwds)
            opts = {"product": self.product, "start_jar": self.start_jar, "end_jar": self.end_jar, "crate": self.crate_number}
            try:
                call_command("add_new_jars", stdout=self.out, **opts)
            except CommandError as e:
                self.assertEqual(e.args[0], self.error)
            else:
                self.fail("Should have failed with {0}".format(self.error))
            self.assertEqual(self.good_crate.jars, self.good_crate_jars)

        return _decorator

    @anj_ce
    def test_anj_ce_product_required(self):
        self.product = ""
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = "Product required!"

    @anj_ce
    def test_anj_ce_not_valid_product(self):
        # Try adding non-existent product to good crate.
        self.product = self.bad_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = "Not a valid product: {0}".format(self.product)

    @anj_ce
    def test_anj_ce_start_jar_not_int(self):
        # Start jar is not an int.
        self.product = self.good_product_name
        self.start_jar = "x"
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = "Start jar and end jar must be ints!"

    @anj_ce
    def test_anj_ce_end_jar_not_int(self):
        # End jar is not an int.
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = "x"
        self.crate_number = self.good_crate_number
        self.error = "Start jar and end jar must be ints!"

    @anj_ce
    def test_anj_ce_start_and_end_jar_both_not_ints(self):
        # End jar is not an int.
        self.product = self.good_product_name
        self.start_jar = ""
        self.end_jar = ""
        self.crate_number = self.good_crate_number
        self.error = "Start jar and end jar must be ints!"

    @anj_ce
    def test_anj_ce_start_not_less_than_end(self):
        # Try a start jar that's greater than an end jar.
        self.product = self.good_product_name
        self.start_jar = self.good_end_jar
        self.end_jar = self.good_start_jar
        self.crate_number = self.good_crate_number
        self.error = "Start jar value must be less than or equal to end jar value"

    @anj_ce
    def test_anj_ce_crate_not_int(self):
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar
        self.crate_number = "x"
        self.error = "Crate value is not an int: {0}".format(self.crate_number)

    @anj_ce
    def test_anj_ce_already_exist(self):
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar - 1
        self.end_jar = self.good_end_jar
        self.crate_number = self.good_crate_number
        self.error = "Jars already exist in this product within this range"

    @anj_ce
    def test_anj_ce_exceed_capacity(self):
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar + 1
        self.crate_number = self.good_crate_number
        self.error = "Crate capacity would be exceeded: {0} > {1}".format(self.good_crate.capacity + 1, self.good_crate.capacity)

    @anj_ce
    def test_anj_ce_bad_crate(self):
        # Delete the crate and try to add jars to it.
        self.product = self.good_product_name
        self.start_jar = self.good_start_jar
        self.end_jar = self.good_end_jar + 1
        self.crate_number = self.good_crate_number + 10
        self.error = "Not a valid crate: {0}".format(self.crate_number)

    def test_add_new_jars_dry_run(self):
        # Try with dry run enabled.
        # No error should be raised, no new jars should be added.
        opts = {
            "product": self.good_product_name,
            "start_jar": self.good_start_jar,
            "end_jar": self.good_end_jar,
            "crate": self.good_crate_number,
            "dryrun": True,
        }
        call_command("add_new_jars", stdout=self.out, **opts)
        self.assertEqual(self.good_crate.jars, self.good_crate_jars)

    def test_add_new_jars_good(self):
        # No error should be raised, but new jars should be added.
        opts = {"product": self.good_product_name, "start_jar": self.good_start_jar, "end_jar": self.good_end_jar, "crate": self.good_crate_number}
        call_command("add_new_jars", stdout=self.out, **opts)
        self.assertEqual(self.good_crate.jars, self.good_crate_jars + self.num_jars)


class DeleteOldJarsTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.out = StringIO()

    def test_delete_old_jars(self):
        all_count = Jar.objects.count()
        remove_before = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        deletable_count = Jar.objects.filter(is_active=False, updated_at__lt=remove_before).count()
        remaining_count = all_count - deletable_count
        # Try with dry run enabled.
        # No error should be raised, no jars should be deleted.
        opts = {"dryrun": True}
        call_command("delete_old_jars", stdout=self.out, **opts)
        self.assertEqual(Jar.objects.all().count(), all_count)
        # Try without dry run enabled.
        # No error should be raised, all jars should be deleted.
        call_command("delete_old_jars", stdout=self.out)
        self.assertEqual(Jar.objects.all().count(), remaining_count)


class CrateUtilizationTestCase(TestCase):
    fixtures = ["inventory", "meadery"]

    def setUp(self):
        self.out = StringIO()
        self.good_warehouse_number = Warehouse.objects.get(number=2).number

    # crate_utilization_commanderror
    def cu_ce(func):
        def _decorator(self, *args, **kwds):
            func(self, *args, **kwds)
            opts = {}
            try:
                opts["warehouse"] = self.warehouse_number
            except AttributeError:
                pass
            try:
                call_command("crate_utilization", stdout=self.out, **opts)
            except CommandError as e:
                self.assertEqual(e.args[0], self.error)
            else:
                self.fail("Should have failed with {0}".format(self.error))

        return _decorator

    @cu_ce
    def test_cu_ce_not_int(self):
        self.warehouse_number = "x"
        self.error = "Warehouse not an int: {0}".format(self.warehouse_number)

    @cu_ce
    def test_cu_ce_does_not_exist(self):
        self.warehouse_number = self.good_warehouse_number + 10
        self.error = "Not a valid warehouse number: {0}".format(self.warehouse_number)

    def cu_good(empty, full):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                func(self, *args, **kwds)
                opts = {"warehouse": self.good_warehouse_number}
                if empty:
                    opts["empty"] = True
                if full:
                    opts["full"] = True
                try:
                    call_command("crate_utilization", stdout=self.out, **opts)
                except CommandError as e:
                    self.fail("Failed with {0}".format(e.args[0]))
                self.assertEqual(self.expected_default, self.out.getvalue())

            return _decorator

        return real_decorator

    @cu_good(False, False)
    def test_crate_utilization_neither(self):
        self.expected_default = (
            "Crate ID |         Bin         | Capacity | Jars \n==================================================\n"
            + "    1    | Row 1 Shelf 2 Bin 1 |    11    |  3   \n"
        )

    @cu_good(True, False)
    def test_crate_utilization_empty(self):
        self.expected_default = (
            "Crate ID |         Bin         | Capacity | Jars \n==================================================\n"
            + "    2    | Row 2 Shelf 1 Bin 1 |    12    |  0   \n    1    | Row 1 Shelf 2 Bin 1 |    11    |  3   \n"
        )

    @cu_good(False, True)
    def test_crate_utilization_full(self):
        self.expected_default = (
            "Crate ID |         Bin         | Capacity | Jars \n==================================================\n"
            + "    1    | Row 1 Shelf 2 Bin 1 |    11    |  3   \n    3    | Row 1 Shelf 1 Bin 1 |    12    |  12  \n"
        )

    @cu_good(True, True)
    def test_crate_utilization_both(self):
        self.expected_default = (
            "Crate ID |         Bin         | Capacity | Jars \n==================================================\n"
            + "    2    | Row 2 Shelf 1 Bin 1 |    12    |  0   \n    1    | Row 1 Shelf 2 Bin 1 |    11    |  3   \n"
            + "    3    | Row 1 Shelf 1 Bin 1 |    12    |  12  \n"
        )
