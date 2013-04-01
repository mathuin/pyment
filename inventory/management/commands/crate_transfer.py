from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
from catalog.models import Product
from optparse import make_option

class Command(BaseCommand):
    args = '<source number> <dest number>'
    help = 'Move jars from one crate to another.'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', 
                    action='store_true', 
                    dest='dryrun', 
                    default=False, 
                    help='Simulate the command'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Wrong number of arguments')
        try:
            source_number = args[0]
        except ValueError:
            raise CommandError('Source crate is not an int: %s' % args[0])
        if Crate.objects.filter(number=source_number).exists():
            source = Crate.objects.get(number=source_number)
        else:
            raise CommandError('Source crate not valid: %d' % source_number)
        try:
            dest_number = args[1]
        except ValueError:
            raise CommandError('Destination crate is not an int: %s' % args[1])
        if Crate.objects.filter(number=dest_number).exists():
            dest = Crate.objects.get(number=dest_number)
        else:
            raise CommandError('Destination crate not valid: %d' % dest_number)
        if source.jars + dest.jars > dest.capacity:
            raise CommandError('Destination crate does not have enough room')
        if not Jar.objects.filter(crate=source).exists():
            raise CommandError('Source crate is empty')
        source_jars = Jar.objects.filter(crate=source)
        if not options['dryrun']:
            for jar in source_jars:
                jar.crate = dest
                jar.save()
        self.stdout.write('%d jars were moved from crate %d to crate %d' % (len(source_jars), source_number, dest_number))
