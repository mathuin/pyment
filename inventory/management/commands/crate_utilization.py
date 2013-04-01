from django.core.management.base import BaseCommand, CommandError
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from optparse import make_option

class Command(BaseCommand):
    args = '<warehouse number>'
    help = 'Generates a crate utilization table for the specified warehouse.'
    option_list = BaseCommand.option_list + (
        make_option('--full', 
                    action='store_true', 
                    dest='full', 
                    default=False, 
                    help='Include full crates in table'),
        make_option('--empty', 
                    action='store_true', 
                    dest='empty', 
                    default=False, 
                    help='Include empty crates in table'),
        )

    def handle(self, *args, **options):
        
        if len(args) != 1:
            raise CommandError('Wrong number of arguments')
        try:
            warehouse_number = int(args[0])
        except ValueError:
            raise CommandError('Argument not an int: %s' % args[0])
        if Warehouse.objects.filter(number=warehouse_number).exists():
            warehouse = Warehouse.objects.get(number=warehouse_number)
        else:
            raise CommandError('Not a valid warehouse number: %d' % warehouse_number)
        # actually do the work
        # NB: these values are hand-crafted
        # need to find a better way to calculate them on the fly
        # they will break if row/shelf/bin exceeds one digit in length
        fieldwidths = (9, 21, 10, 6)
        headerformat = '{0:^%ds}|{1:^%ds}|{2:^%ds}|{3:^%ds}\n' % fieldwidths
        dataformat = '{0:^%dd}|{1:^%ds}|{2:^%dd}|{3:^%dd}\n' % fieldwidths
        headerline = headerformat.format('Crate ID', 'Bin', 'Capacity', 'Jars')
        self.stdout.write(headerline)
        self.stdout.write('='*len(headerline))
        for crate in sorted(Crate.objects.filter(bin__in=Bin.objects.filter(shelf__in=Shelf.objects.filter(row__in=Row.objects.filter(warehouse=warehouse)))), key=lambda c: c.jars*1.0/c.capacity):
            if (crate.jars != crate.capacity and crate.jars != 0) or (options['full'] and crate.jars == crate.capacity) or (options['empty'] and crate.jars == 0):
                # The warehouse is superfluous here
                loc = crate.bin.longname[len(warehouse.longname):]
                self.stdout.write(dataformat.format(crate.id, loc, crate.capacity, crate.jars))
