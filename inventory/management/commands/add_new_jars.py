from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
from catalog.models import Product

class Command(BaseCommand):
    args = '<product> <start_jar> <end_jar> <crate>'
    help = 'Creates new jars in a particular product placing them in a particular crate'

    def handle(self, *args, **options):
        if len(args) != 4:
            raise CommandError, 'Wrong number of arguments'
        product_name = args[0]
        brewname, batchletter = product_name.rsplit(' ', 1)
        if Product.objects.filter(brewname=brewname, batchletter=batchletter).exists():
            product = Product.objects.get(brewname=brewname, batchletter=batchletter)
        else:
            raise CommandError, 'Not a valid product: %s' % product_name
        # check that jar arguments are valid
        try:
            start_jar = int(args[1])
        except ValueError:
            raise CommandError, 'Start jar value is not an int: %s' % args[1]
        try:
            end_jar = int(args[2])
        except ValueError:
            raise CommandError, 'End jar value is not an int: %s' % args[2]
        if (end_jar - start_jar >= 0):
            jar_list = [x for x in xrange(start_jar, end_jar+1)]
        else:
            raise CommandError, 'Start jar value must be less than or equal to end jar value'
        if Jar.objects.filter(product=product, number__in=jar_list).exists():
            raise CommandError, 'Jars already exist in this product within this range'
        crate_name = args[3]
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
        self.stdout.write('%s jars were created in %s and placed in %s\n' % (len(jar_list), product, crate))
