from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
from catalog.models import Product

class Command(BaseCommand):
    args = '<product> <start_jar> <end_jar> <crate>'
    help = 'Creates new jars in a particular product placing them in a particular crate'

    def handle(self, *args, **options):
        if len(args) != 4:
            raise CommandError, 'Wrong number of arguments'
        print args
        if isinstance(args[0], basestring):
            product_name = args[0]
        else:
            raise CommandError, 'Product name is not a string: %s' % args[0]
        brewname, batchletter = product_name.rsplit(' ', 1)
        if Product.objects.filter(brewname=brewname, batchletter=batchletter).exists():
            product = Product.objects.get(brewname=brewname, batchletter=batchletter)
        else:
            raise CommandError, 'Not a valid product: %s' % product_name
        # check that jar arguments are valid
        if isinstance(args[1], int):
            start_jar = args[1]
        else:
            raise CommandError, 'Start jar value is not an int: %s' % args[1]
        if isinstance(args[2], int):
            end_jar = args[2]
        else:
            raise CommandError, 'End jar value is not an int: %s' % args[2]
        if (end_jar - start_jar >= 0):
            jar_list = [x for x in xrange(start_jar, end_jar+1)]
        else:
            raise CommandError, 'Start jar value must be less than or equal to end jar value'
        if Jar.objects.filter(product=product, number__in=jar_list).exists():
            raise CommandError, 'Jars already exist in this product within this range'
        if isinstance(args[3], basestring):
            crate_name = args[3]
        else:
            raise CommandError, 'Crate name is not a string: %s' % args[3]
        _, cratenumber = crate_name.split(' ', 1)
        if Crate.objects.filter(number=cratenumber).exists():
            crate = Crate.objects.get(number=cratenumber)
        else:
            raise CommandError, 'Not a valid crate: %s' % crate_name
        if (crate.jars + len(jar_list)) > crate.capacity:
            raise CommandError, 'Crate capacity would be exceeded: %d > %d' % (crate.jars + len(jar_list), crate.capacity)
        # actually do the work
        for jar_number in jar_list:
            jar = Jar(product=product, number=jar_number, crate=crate, is_active=True, is_available=True)
            jar.save()
        self.stdout.write('%s jars were created in product %s and placed in crate %s\n' % (len(jar_list), product, crate))
