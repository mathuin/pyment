from django.core.management.base import NoArgsCommand
from inventory.models import Product
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc
from optparse import make_option

class Command(NoArgsCommand):
    help = 'Disable products with no active jars remaining'
    option_list = NoArgsCommand.option_list + (
        make_option('--dry-run', 
                    action='store_true', 
                    dest='dryrun', 
                    default=False, 
                    help='Simulate the command'),
        )

    def handle(self, **options):
        self.stdout.write('Disabling inactive products\n')
        # All active products without active jars
        old_products = Product.active.exclude(jar__is_active=True)
        if not options['dryrun']:
            for product in old_products:
                product.is_active=False
                product.save()
        self.stdout.write('%s products were disabled\n' % len(old_products))
