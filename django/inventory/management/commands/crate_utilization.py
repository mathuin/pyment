from django.core.management.base import BaseCommand, CommandError
from inventory.models import Warehouse, Row, Shelf, Bin, Crate


class Command(BaseCommand):
    help = 'Generates a crate utilization table for the specified warehouse.'

    def add_arguments(self, parser):
        parser.add_argument('--warehouse',
                            help='Warehouse for which table is generated.')
        parser.add_argument('--full',
                            action='store_true',
                            dest='full',
                            default=False,
                            help='Include full crates in table')
        parser.add_argument('--empty',
                            action='store_true',
                            dest='empty',
                            default=False,
                            help='Include empty crates in table')

    def handle(self, *args, **options):
        try:
            warehouse = Warehouse.objects.get(number=options['warehouse'])
        except ValueError:
            raise CommandError('Warehouse not an int: %s' % options['warehouse'])
        except KeyError:
            raise CommandError('Warehouse required!')
        except Warehouse.DoesNotExist:
            raise CommandError('Not a valid warehouse number: %s' % options['warehouse'])
        # actually do the work
        # NB: these values are hand-crafted
        # need to find a better way to calculate them on the fly
        # they will break if row/shelf/bin exceeds one digit in length
        fieldwidths = (9, 21, 10, 6)
        headerformat = '{0:^%ds}|{1:^%ds}|{2:^%ds}|{3:^%ds}\n' % fieldwidths
        dataformat = '{0:^%dd}|{1:^%ds}|{2:^%dd}|{3:^%dd}\n' % fieldwidths
        headerline = headerformat.format('Crate ID', 'Bin', 'Capacity', 'Jars')
        self.stdout.write(headerline)
        self.stdout.write('=' * len(headerline))
        for crate in sorted(Crate.objects.filter(bin__in=Bin.objects.filter(shelf__in=Shelf.objects.filter(row__in=Row.objects.filter(warehouse=warehouse)))), key=lambda c: c.jars * 1.0 / c.capacity):
            if (crate.jars != crate.capacity and crate.jars != 0) or (options['full'] and crate.jars == crate.capacity) or (options['empty'] and crate.jars == 0):
                # The warehouse is superfluous here
                loc = crate.bin.longname[len(warehouse.longname) + 1:]
                self.stdout.write(dataformat.format(crate.id, loc, crate.capacity, crate.jars))
