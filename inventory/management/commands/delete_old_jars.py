from django.core.management.base import BaseCommand
from inventory.models import Jar
from pyment import settings
from django.utils import timezone
from datetime import timedelta
from optparse import make_option


class Command(BaseCommand):
    help = 'Delete inactive jars more than %d days old' % settings.INACTIVE_JAR_AGE_DAYS
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
                    action='store_true',
                    dest='dryrun',
                    default=False,
                    help='Simulate the command'),
    )

    def handle(self, **options):
        self.stdout.write('Removing inactive jars\n')
        # calculate date of INACTIVE_JAR_AGE_DAYS days ago
        remove_before = timezone.now() + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        old_jars = Jar.objects.filter(is_active=False, updated_at__lt=remove_before)
        if not options['dryrun']:
            old_jars.delete()
        self.stdout.write('%d jars were removed\n' % len(old_jars))
