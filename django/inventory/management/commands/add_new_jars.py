from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
from meadery.models import Product


class Command(BaseCommand):
    args = "<product> <start_jar> <end_jar> <crate number>"
    help = "Creates new jars in a particular product placing them in a particular crate"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", dest="dryrun", default=False, help="Simulate the command")
        parser.add_argument("--product", dest="product", help="Product to be added")
        parser.add_argument("--start-jar", dest="start_jar", type=int, help="First jar sequence number to be added")
        parser.add_argument("--end-jar", dest="end_jar", type=int, help="Last jar sequence number to be added")
        parser.add_argument("--crate", type=int, help="Crate number where new product will be added")

    def handle(self, *args, **options):
        try:
            (brewname, batchletter) = options["product"].rsplit(" ", 1)
            product = Product.objects.get(brewname=brewname, batchletter=batchletter)
        except ValueError:
            raise CommandError("Product required!")
        except Product.DoesNotExist:
            raise CommandError("Not a valid product: %s" % options["product"])

        try:
            start_jar = options["start_jar"]
        except ValueError:
            raise CommandError("Start jar value is not an int: %s" % options["start_jar"])
        try:
            end_jar = options["end_jar"]
        except ValueError:
            raise CommandError("End jar value is not an int: %s" % options["end_jar"])
        try:
            jar_list = [x for x in range(start_jar, end_jar + 1)]
        except NameError:
            raise CommandError("Start jar and end jar required!")
        except TypeError:
            raise CommandError("Start jar and end jar must be ints!")

        if jar_list == []:
            raise CommandError("Start jar value must be less than or equal to end jar value")

        if Jar.objects.filter(product=product, number__in=jar_list).exists():
            raise CommandError("Jars already exist in this product within this range")

        try:
            crate = Crate.objects.get(number=options["crate"])
        except ValueError:
            raise CommandError("Crate value is not an int: %s" % options["crate"])
        except Crate.DoesNotExist:
            raise CommandError("Not a valid crate: %s" % options["crate"])

        if (crate.jars + len(jar_list)) > crate.capacity:
            raise CommandError("Crate capacity would be exceeded: %d > %d" % (crate.jars + len(jar_list), crate.capacity))

        # actually do the work
        for jar_number in jar_list:
            if not options["dryrun"]:
                jar = Jar(product=product, number=jar_number, crate=crate, is_active=True, is_available=True)
                jar.save()
        self.stdout.write("%d jars were created in %s and placed in %s\n" % (len(jar_list), product, crate))
