from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
from meadery.models import Product
from optparse import make_option


class Command(BaseCommand):
    args = '<product> <start_jar> <end_jar> <crate number>'
    help = 'Creates new jars in a particular product placing them in a particular crate'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
                    action='store_true',
                    dest='dryrun',
                    default=False,
                    help='Simulate the command'),
        make_option('--product',
                    dest='product',
                    help='Product to be added'),
        make_option('--start-jar',
                    dest='start_jar',
                    type='int',
                    help='First jar sequence number to be added'),
        make_option('--end-jar',
                    dest='end_jar',
                    type='int',
                    help='Last jar sequence number to be added'),
        make_option('--crate',
                    type='int',
                    help='Crate number where new product will be added'),
    )

    def handle(self, *args, **options):
        if options['product']:
            (brewname, batchletter) = options['product'].rsplit(' ', 1)
        else:
            raise CommandError('Product required!')
        try:
            product = Product.objects.get(brewname=brewname, batchletter=batchletter)
        except Product.DoesNotExist:
            raise CommandError('Not a valid product: %s' % options['product'])
        if options['start_jar']:
            if isinstance(options['start_jar'], (int, long)):
                start_jar = options['start_jar']
            else:
                raise CommandError('Start jar value is not an int: %s' % options['start_jar'])
        else:
            raise CommandError('Start jar required!')
        if options['end_jar']:
            if isinstance(options['end_jar'], (int, long)):
                end_jar = options['end_jar']
            else:
                raise CommandError('End jar value is not an int: %s' % options['end_jar'])
        else:
            raise CommandError('End jar required!')
        if (end_jar - start_jar >= 0):
            jar_list = [x for x in xrange(start_jar, end_jar+1)]
        else:
            raise CommandError('Start jar value must be less than or equal to end jar value')
        if Jar.objects.filter(product=product, number__in=jar_list).exists():
            raise CommandError('Jars already exist in this product within this range')
        if options['crate']:
            if isinstance(options['crate'], (int, long)):
                crate_number = options['crate']
            else:
                raise CommandError('Crate value is not an int: %s' % options['crate'])
        else:
            raise CommandError('Crate required!')
        try:
            crate = Crate.objects.get(number=crate_number)
        except Crate.DoesNotExist:
            raise CommandError('Not a valid crate: %d' % crate_number)
        if (crate.jars + len(jar_list)) > crate.capacity:
            raise CommandError('Crate capacity would be exceeded: %d > %d' % (crate.jars + len(jar_list), crate.capacity))
        # actually do the work
        for jar_number in jar_list:
            if not options['dryrun']:
                jar = Jar(product=product, number=jar_number, crate=crate, is_active=True, is_available=True)
                jar.save()
        self.stdout.write('%d jars were created in %s and placed in %s\n' % (len(jar_list), product, crate))
