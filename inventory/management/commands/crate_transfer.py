from django.core.management.base import BaseCommand, CommandError
from inventory.models import Jar, Crate
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
        make_option('--source',
                    dest='source',
                    type='int',
                    help='Crate from which jars are moved'),
        make_option('--dest',
                    dest='dest',
                    type='int',
                    help='Crate to which jars are moved'),
    )

    def handle(self, *args, **options):
        try:
            source = Crate.objects.get(number=options['source'])
        except ValueError:
            raise CommandError('Source crate is not an int: %s' % options['source'])
        except KeyError:
            raise CommandError('Source crate required!')
        except Crate.DoesNotExist:
            raise CommandError('Source crate not valid: %s' % options['source'])

        try:
            dest = Crate.objects.get(number=options['dest'])
        except ValueError:
            raise CommandError('Dest crate is not an int: %s' % options['dest'])
        except KeyError:
            raise CommandError('Dest crate required!')
        except Crate.DoesNotExist:
            raise CommandError('Dest crate not valid: %s' % options['dest'])

        if source.jars == 0:
            raise CommandError('Source crate is empty')
        if source.jars + dest.jars > dest.capacity:
            raise CommandError('Destination crate does not have enough room')
        source_jars = Jar.objects.filter(crate=source)
        if not options['dryrun']:
            for jar in source_jars:
                jar.crate = dest
                jar.save()
        self.stdout.write('%d jars were moved from %s to %s' % (len(source_jars), source, dest))
